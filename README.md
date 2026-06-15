# Submarine Cable Resilience Analyzer

NetworkX graph analysis of global submarine cable infrastructure. Betweenness centrality identifies physical chokepoints in the network that carries 99% of international internet traffic. N-1/N-2 cable cut simulations quantify connectivity and capacity loss. Interactive Folium map with risk heat layer.

**This tool is distinct from [FriendShore](https://github.com/JakPot42/friendshore-supply-chain).** FriendShore traces corporate supply chain relationships — which companies depend on which Tier-2 and Tier-3 suppliers. This tool analyzes physical undersea network topology — which landing stations are chokepoints in the global internet's physical layer, and what happens when specific cables are severed.

**Live demo:** [cable-resilience.onrender.com](https://cable-resilience.onrender.com)

---

## What it does

1. **NetworkX graph** — Landing stations as nodes, cable segments as weighted edges (weight = 1/capacity, so high-capacity routes are preferred paths)
2. **Betweenness centrality** — Identifies landing stations that lie on the most shortest paths; ranks global chokepoints
3. **N-1/N-2 simulation** — Remove 1 or 2 cables from the graph; measure disconnected station pairs, isolated nodes, and total Tbps capacity lost
4. **Interactive Folium map** — Cable paths with hover tooltips; stations colored by risk level; cut cables shown in red/dashed; isolated stations in purple
5. **Risk scoring** — Deterministic engine scores each landing station on centrality (40 pts), cable count (30 pts), jurisdiction risk (15 pts), and chokepoint geography (15 pts)
6. **Strategic brief** — Claude Haiku analyzes simulation results and drafts a 2-3 paragraph infrastructure resilience assessment; pre-baked for demo scenarios

---

## Architecture distinction: FriendShore vs. Cable Resilience

| | FriendShore | Cable Resilience Analyzer |
|---|---|---|
| Domain | Corporate supply chain | Physical network topology |
| Nodes | Companies (suppliers) | Landing stations |
| Edges | Supplier relationships | Cable segments |
| Risk | High-risk country SPF, single-source dependency | Betweenness centrality, geographic chokepoints |
| Graph | Directed, hierarchical (Tier 1/2/3) | Undirected, weighted by capacity |
| Use case | BOM analysis, procurement | Undersea infrastructure protection |

---

## Demo scenarios (pre-seeded)

| Scenario | Cables Cut | Type | Modeled After |
|---|---|---|---|
| Taiwan Strait Severance | TPE + NCP | N-2 | Taiwan Strait conflict scenario |
| Red Sea Corridor Disruption | SEA-ME-WE 5 + AAE-1 | N-2 | 2024 Houthi cable attacks |
| Singapore Hub Failure | TPE + APCN-2 + AAG | N-3 | Hub-and-spoke concentration risk |

---

## NUWC / DoD relevance

The Naval Undersea Warfare Center (NUWC) at Newport, RI leads Navy programs in undersea domain awareness, including passive surveillance of undersea infrastructure. CISA's Critical Infrastructure Security and Resilience (CISR) directorate identifies submarine cables as Tier-1 national security infrastructure.

This tool surfaces the same chokepoint analysis — betweenness centrality on physical network topology — that CISA uses in its National Infrastructure Protection Plan undersea cable assessments.

Key findings from this dataset:
- **Djibouti** (Bab el-Mandeb): gateway for Asia-Europe-Africa cables, CRITICAL by centrality + jurisdiction + chokepoint geography
- **Alexandria, Egypt** (Suez corridor): convergence of 6 cable systems, CRITICAL
- **Singapore** (Strait of Malacca): 6+ cable systems, highest centrality in dataset, CRITICAL
- **Virginia Beach, VA**: primary US East Coast landing hub for 5 transatlantic cables, HIGH

---

## Architecture

```
cable_analyzer/
├── config.py          — risk weights, HIGH_RISK_COUNTRIES, CHOKEPOINT_SCORES
├── cable_data.py      — 20 cables, 55 landing stations (TeleGeography public data)
├── graph_engine.py    — build_graph(), betweenness_centrality(), cable_counts_per_station()
├── simulation.py      — run_simulation() → SimulationResult (capacity, pairs, isolation)
├── risk_engine.py     — score_landing_station() (4-component deterministic scoring)
├── map_generator.py   — generate_global_map() / generate_scenario_map() → Folium HTML
├── claude_analyst.py  — generate_resilience_brief() (Claude Haiku, catches Exception)
├── seed_data.py       — DEMO_SCENARIOS with pre-baked briefs
├── pdf_export.py      — ReportLab Supplier Resilience Report with DEMO watermark
└── main.py            — FastAPI app, startup caching, custom simulation form
```

---

## Running locally

```bash
git clone https://github.com/JakPot42/cable-resilience
cd cable-resilience
pip install -r requirements.txt
uvicorn cable_analyzer.main:app --reload
# Open http://localhost:8000
```

Set `ANTHROPIC_API_KEY` to enable live Claude brief generation for custom simulations.

---

## Tests

```bash
pytest tests/ -v
```

All provider/Claude calls are mocked. Tests cover cable data integrity, graph construction, simulation mechanics, risk scoring, map generation, and seed scenario validation.

---

## Honest limitations

- Dataset covers 20 major cables from TeleGeography public data (June 2026). Global infrastructure includes 500+ cables — this is a representative sample, not a complete model
- Cable paths use simplified waypoints; actual routes follow ocean floor topology
- Betweenness centrality assumes shortest-path routing; actual internet traffic uses BGP policies that deviate from shortest path
- Capacity figures are published design capacity, not current utilization
- 13F ownership and financial risk factors (from DIB Monitor) are not integrated here — a production tool would bridge both layers
- DEMO_MODE = True in all public deployment; not for operational use
