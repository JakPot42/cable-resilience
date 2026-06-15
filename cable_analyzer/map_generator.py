from __future__ import annotations

import folium
import networkx as nx

LEVEL_COLORS = {
    "CRITICAL": "#dc2626",   # red-600
    "HIGH":     "#ea580c",   # orange-600
    "MEDIUM":   "#ca8a04",   # yellow-600
    "LOW":      "#16a34a",   # green-600
}

CABLE_COLOR   = "#2563eb"  # blue-600
CUT_COLOR     = "#dc2626"  # red-600
ACTIVE_COLOR  = "#2563eb"


def _add_cables(m: folium.Map, cables: list[dict], cut_ids: set[str] | None = None) -> None:
    if cut_ids is None:
        cut_ids = set()
    for cable in cables:
        coords = cable.get("path_coords", [])
        if len(coords) < 2:
            continue
        is_cut = cable["id"] in cut_ids
        folium.PolyLine(
            locations=coords,
            color=CUT_COLOR if is_cut else ACTIVE_COLOR,
            weight=4 if is_cut else 2,
            opacity=0.9 if is_cut else 0.65,
            dash_array="10 5" if is_cut else None,
            tooltip=f"{'[CUT] ' if is_cut else ''}{cable['name']} "
                    f"({cable.get('capacity_tbps', '?')} Tbps, {cable.get('rfs_year', '?')})",
        ).add_to(m)


def _add_stations(
    m: folium.Map,
    landing_points: list[dict],
    risk_scores: dict[str, dict],
    isolated_ids: set[str] | None = None,
) -> None:
    if isolated_ids is None:
        isolated_ids = set()
    for lp in landing_points:
        lp_id = lp["id"]
        risk = risk_scores.get(lp_id, {})
        level = risk.get("level", "LOW")
        score = risk.get("score", 0)
        is_isolated = lp_id in isolated_ids
        color = "#7c3aed" if is_isolated else LEVEL_COLORS.get(level, "#16a34a")
        radius = 9 if is_isolated or level in ("CRITICAL", "HIGH") else 6

        popup_html = (
            f"<b>{lp['name']}</b><br>"
            f"{lp.get('country', '')}<br>"
            f"Risk: <b>{level}</b> ({score}/100)"
        )
        if is_isolated:
            popup_html = f"<b>⚠ ISOLATED</b><br>{popup_html}"

        folium.CircleMarker(
            location=(lp["lat"], lp["lon"]),
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"{'[ISOLATED] ' if is_isolated else ''}{lp['name']} — {level}",
        ).add_to(m)


def generate_global_map(
    G: nx.Graph,
    landing_points: list[dict],
    cables: list[dict],
    risk_scores: dict[str, dict],
) -> str:
    """Render all cables + landing stations colored by risk level. Returns HTML string."""
    m = folium.Map(location=[20, 10], zoom_start=2, tiles="CartoDB positron")
    _add_cables(m, cables)
    _add_stations(m, landing_points, risk_scores)
    _add_legend(m)
    return m.get_root().render()


def generate_scenario_map(
    landing_points: list[dict],
    cables: list[dict],
    cut_cable_ids: list[str],
    isolated_lp_ids: list[str],
    risk_scores: dict[str, dict],
) -> str:
    """Render scenario: cut cables in red/dashed, isolated stations in purple. Returns HTML string."""
    m = folium.Map(location=[20, 10], zoom_start=2, tiles="CartoDB positron")
    _add_cables(m, cables, cut_ids=set(cut_cable_ids))
    _add_stations(m, landing_points, risk_scores, isolated_ids=set(isolated_lp_ids))
    _add_legend(m, scenario=True)
    return m.get_root().render()


def _add_legend(m: folium.Map, scenario: bool = False) -> None:
    items = [
        ('<span style="color:#dc2626">●</span>', "CRITICAL"),
        ('<span style="color:#ea580c">●</span>', "HIGH"),
        ('<span style="color:#ca8a04">●</span>', "MEDIUM"),
        ('<span style="color:#16a34a">●</span>', "LOW"),
    ]
    if scenario:
        items += [
            ('<span style="color:#7c3aed">●</span>', "ISOLATED"),
            ('<span style="color:#dc2626; text-decoration:line-through">——</span>', "Cut cable"),
        ]
    else:
        items += [('<span style="color:#2563eb">——</span>', "Cable route")]

    rows = "".join(f"<tr><td>{icon}</td><td>{label}</td></tr>" for icon, label in items)
    legend_html = f"""
    <div style="position:fixed;bottom:30px;right:10px;z-index:1000;
                background:white;padding:8px 12px;border-radius:6px;
                box-shadow:0 2px 6px rgba(0,0,0,.3);font-size:12px;">
      <b>Legend</b><br><table>{rows}</table>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
