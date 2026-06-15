from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates

from .cable_data import CABLES, CABLE_BY_ID, LANDING_POINTS, LANDING_POINT_BY_ID
from .graph_engine import (
    build_graph,
    compute_betweenness_centrality,
    cable_counts_per_station,
    top_chokepoints,
)
from .map_generator import generate_global_map, generate_scenario_map
from .risk_engine import score_all_stations
from .simulation import run_simulation
from .seed_data import DEMO_SCENARIOS, DEMO_SCENARIO_BY_ID
from .claude_analyst import generate_resilience_brief, AnalystError
from .pdf_export import generate_report

# ── App-level state (computed once at startup) ───────────────────────────────
_state: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    G = build_graph(CABLES, LANDING_POINTS)
    centrality = compute_betweenness_centrality(G)
    counts = cable_counts_per_station(CABLES, LANDING_POINTS)
    risk_scores = score_all_stations(LANDING_POINTS, centrality, counts)

    global_map_html = generate_global_map(G, LANDING_POINTS, CABLES, risk_scores)
    chokepoints = top_chokepoints(centrality, risk_scores, n=10)

    # Pre-compute all demo scenario results
    scenario_results: dict[str, Any] = {}
    scenario_maps: dict[str, str] = {}
    for s in DEMO_SCENARIOS:
        result = run_simulation(s["cable_cuts"], scenario_id=s["id"], G=G)
        result.brief = s["pre_baked_brief"]
        scenario_results[s["id"]] = result
        scenario_maps[s["id"]] = generate_scenario_map(
            LANDING_POINTS, CABLES,
            cut_cable_ids=s["cable_cuts"],
            isolated_lp_ids=result.isolated_node_ids,
            risk_scores=risk_scores,
        )

    _state.update({
        "G": G,
        "centrality": centrality,
        "counts": counts,
        "risk_scores": risk_scores,
        "global_map_html": global_map_html,
        "chokepoints": chokepoints,
        "scenario_results": scenario_results,
        "scenario_maps": scenario_maps,
    })
    yield


DEMO_MODE = os.getenv("DEMO_MODE", "True").lower() in ("1", "true", "yes")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

app = FastAPI(
    title="Submarine Cable Resilience Analyzer",
    lifespan=lifespan,
)
templates = Jinja2Templates(directory="templates")


# ── Global map (served as standalone HTML, embedded via iframe) ───────────────
@app.get("/map", response_class=HTMLResponse)
async def global_map_page():
    return HTMLResponse(_state["global_map_html"])


@app.get("/scenario/{scenario_id}/map", response_class=HTMLResponse)
async def scenario_map_page(scenario_id: str):
    if scenario_id in _state["scenario_maps"]:
        return HTMLResponse(_state["scenario_maps"][scenario_id])
    raise HTTPException(status_code=404, detail="Scenario not found")


# ── Main pages ────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {
        "chokepoints": _state["chokepoints"],
        "scenarios": DEMO_SCENARIOS,
        "total_cables": len(CABLES),
        "total_stations": len(LANDING_POINTS),
        "demo_mode": DEMO_MODE,
    })


@app.get("/scenario/{scenario_id}", response_class=HTMLResponse)
async def scenario_detail(request: Request, scenario_id: str):
    scenario = DEMO_SCENARIO_BY_ID.get(scenario_id)
    result = _state["scenario_results"].get(scenario_id)
    if not scenario or not result:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return templates.TemplateResponse(request, "scenario.html", {
        "scenario": scenario,
        "result": result,
        "demo_mode": DEMO_MODE,
    })


@app.get("/station/{lp_id}", response_class=HTMLResponse)
async def station_detail(request: Request, lp_id: str):
    lp = LANDING_POINT_BY_ID.get(lp_id)
    if not lp:
        raise HTTPException(status_code=404, detail="Landing station not found")
    from .graph_engine import get_cables_for_station
    cables_here = get_cables_for_station(lp_id, CABLES)
    risk = _state["risk_scores"].get(lp_id, {})
    centrality = _state["centrality"].get(lp_id, 0.0)
    return templates.TemplateResponse(request, "station.html", {
        "lp": lp,
        "cables": cables_here,
        "risk": risk,
        "centrality": round(centrality, 5),
        "demo_mode": DEMO_MODE,
    })


# ── Custom simulation ─────────────────────────────────────────────────────────
@app.post("/simulate", response_class=HTMLResponse)
async def simulate(
    request: Request,
    cable_ids: list[str] = Form(...),
):
    if not cable_ids or all(c == "" for c in cable_ids):
        raise HTTPException(status_code=400, detail="Select at least one cable to cut")

    # Validate
    invalid = [c for c in cable_ids if c not in CABLE_BY_ID]
    if invalid:
        raise HTTPException(status_code=400, detail=f"Unknown cable ID(s): {invalid}")

    result = run_simulation(cable_ids, scenario_id="custom", G=_state["G"])

    # Try Claude if key available, else use template text
    if ANTHROPIC_API_KEY and not DEMO_MODE:
        try:
            result.brief = generate_resilience_brief(
                scenario_name=f"Custom N-{len(cable_ids)} simulation",
                cable_names=result.cable_names,
                isolated_stations=result.isolated_node_names,
                disconnected_pairs=result.disconnected_pairs,
                total_pairs=result.total_pairs,
                lost_capacity_tbps=result.lost_capacity_tbps,
                total_capacity_tbps=result.total_capacity_tbps,
                pct_capacity_lost=result.percent_capacity_lost,
                affected_regions=result.affected_regions,
                api_key=ANTHROPIC_API_KEY,
            )
        except AnalystError:
            result.brief = _default_brief(result)
    else:
        result.brief = _default_brief(result)

    scenario_map_html = generate_scenario_map(
        LANDING_POINTS, CABLES,
        cut_cable_ids=cable_ids,
        isolated_lp_ids=result.isolated_node_ids,
        risk_scores=_state["risk_scores"],
    )

    custom_scenario = {
        "id": "custom",
        "name": f"Custom Simulation (N-{len(cable_ids)})",
        "description": f"User-defined cable cut: {', '.join(result.cable_names)}",
        "threat_actor": "Custom",
        "nuwc_relevance": "User-defined scenario.",
        "pre_baked_brief": result.brief,
    }

    return templates.TemplateResponse(request, "scenario.html", {
        "scenario": custom_scenario,
        "result": result,
        "custom_map_html": scenario_map_html,
        "demo_mode": DEMO_MODE,
    })


def _default_brief(result) -> str:
    names = ", ".join(result.cable_names) or "selected cables"
    iso = len(result.isolated_node_ids)
    pct = result.percent_capacity_lost
    return (
        f"This simulation models the simultaneous severance of {names}. "
        f"The result is {iso} isolated landing station(s) and a {pct}% reduction "
        f"in network capacity across the affected segments. "
        f"Set ANTHROPIC_API_KEY to generate a live strategic brief."
    )


# ── PDF download ──────────────────────────────────────────────────────────────
@app.get("/scenario/{scenario_id}/report.pdf")
async def scenario_pdf(scenario_id: str):
    scenario = DEMO_SCENARIO_BY_ID.get(scenario_id)
    result = _state["scenario_results"].get(scenario_id)
    if not scenario or not result:
        raise HTTPException(status_code=404, detail="Scenario not found")
    pdf_bytes = generate_report(result, scenario, result.brief)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="cable-resilience-{scenario_id}.pdf"'},
    )


# ── API stats ─────────────────────────────────────────────────────────────────
@app.get("/api/stats")
async def api_stats():
    return JSONResponse({
        "total_cables": len(CABLES),
        "total_landing_stations": len(LANDING_POINTS),
        "demo_scenarios": len(DEMO_SCENARIOS),
        "demo_mode": DEMO_MODE,
        "top_chokepoints": [
            {"name": c["name"], "level": c["risk_level"]}
            for c in _state["chokepoints"][:5]
        ],
    })
