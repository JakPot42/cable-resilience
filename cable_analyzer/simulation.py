from __future__ import annotations

from dataclasses import dataclass, field

import networkx as nx

from .cable_data import CABLES, LANDING_POINTS, CABLE_BY_ID, LANDING_POINT_BY_ID
from .graph_engine import build_graph


@dataclass
class SimulationResult:
    scenario_id: str
    cable_cuts: list[str]
    cable_names: list[str]

    # Connectivity
    total_nodes: int
    isolated_node_ids: list[str]
    isolated_node_names: list[str]
    components_before: int
    components_after: int

    # Pairs
    total_pairs: int
    disconnected_pairs: int
    percent_pairs_disconnected: float

    # Capacity
    total_capacity_tbps: float
    lost_capacity_tbps: float
    percent_capacity_lost: float

    # Regions / context
    affected_regions: list[str]
    summary_lines: list[str] = field(default_factory=list)

    # Generated brief (from Claude or pre-baked)
    brief: str = ""


def _apply_cuts(G: nx.Graph, cable_cuts: set[str]) -> tuple[nx.Graph, float]:
    """
    Remove edges whose only cable(s) are in cable_cuts.
    Returns modified copy of graph and total capacity lost (Tbps).
    """
    G_cut = G.copy()
    lost_capacity = 0.0

    edges_to_remove: list[tuple] = []
    for u, v, data in G_cut.edges(data=True):
        existing = data.get("cable_ids", [])
        remaining = [cid for cid in existing if cid not in cable_cuts]
        cut_only = [cid for cid in existing if cid in cable_cuts]

        if not remaining:
            edges_to_remove.append((u, v))
            lost_capacity += data.get("capacity_tbps", 0.0)
        else:
            # Reduce capacity by the cut cables' share
            remaining_cap = sum(
                CABLE_BY_ID[cid].get("capacity_tbps", 0.0) for cid in remaining
            )
            cut_cap = sum(
                CABLE_BY_ID[cid].get("capacity_tbps", 0.0) for cid in cut_only
            )
            G_cut[u][v]["cable_ids"] = remaining
            G_cut[u][v]["capacity_tbps"] = remaining_cap
            lost_capacity += cut_cap

    for u, v in edges_to_remove:
        G_cut.remove_edge(u, v)

    return G_cut, lost_capacity


def run_simulation(
    cable_cuts: list[str],
    scenario_id: str = "custom",
    G: nx.Graph | None = None,
    cables: list[dict] | None = None,
    landing_points: list[dict] | None = None,
) -> SimulationResult:
    """
    Simulate cutting the specified cables. Returns a SimulationResult with
    connectivity, capacity, and region impact metrics.
    """
    if cables is None:
        cables = CABLES
    if landing_points is None:
        landing_points = LANDING_POINTS
    if G is None:
        G = build_graph(cables, landing_points)

    cable_cuts_set = set(cable_cuts)
    cable_names = [CABLE_BY_ID[cid]["name"] for cid in cable_cuts if cid in CABLE_BY_ID]

    G_cut, lost_capacity = _apply_cuts(G, cable_cuts_set)

    # Connectivity
    orig_comps = list(nx.connected_components(G))
    cut_comps = list(nx.connected_components(G_cut))
    components_before = len(orig_comps)
    components_after = len(cut_comps)

    # Isolated nodes: nodes with degree 0 after cut
    isolated_ids = [n for n in G_cut.nodes() if G_cut.degree(n) == 0]
    isolated_names = [
        LANDING_POINT_BY_ID.get(lid, {}).get("name", lid) for lid in isolated_ids
    ]

    # Map each node → component index in original graph
    orig_node_component: dict[str, int] = {}
    for idx, comp in enumerate(orig_comps):
        for node in comp:
            orig_node_component[node] = idx

    # Map each node → component index in cut graph
    cut_node_component: dict[str, int] = {}
    for idx, comp in enumerate(cut_comps):
        for node in comp:
            cut_node_component[node] = idx

    # Count disconnected pairs
    nodes = list(G.nodes())
    n = len(nodes)
    total_pairs = n * (n - 1) // 2
    disconnected_pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            a, b = nodes[i], nodes[j]
            # Were connected before?
            if orig_node_component.get(a) == orig_node_component.get(b):
                # Are still connected after?
                if cut_node_component.get(a) != cut_node_component.get(b):
                    disconnected_pairs += 1

    pct_disconnected = round(disconnected_pairs / total_pairs * 100, 2) if total_pairs else 0.0

    # Capacity
    total_capacity = sum(
        data.get("capacity_tbps", 0.0)
        for _, _, data in G.edges(data=True)
    )
    pct_lost = round(lost_capacity / total_capacity * 100, 2) if total_capacity else 0.0

    # Affected regions
    affected_regions = sorted(set(
        LANDING_POINT_BY_ID.get(lid, {}).get("region", "Unknown")
        for lid in isolated_ids
    ))

    # Summary lines
    summary_lines = [
        f"Cables severed: {', '.join(cable_names)}",
        f"Isolated landing stations: {len(isolated_ids)}",
        f"Disconnected station pairs: {disconnected_pairs:,} of {total_pairs:,} ({pct_disconnected}%)",
        f"Capacity lost: {lost_capacity:.1f} Tbps of {total_capacity:.1f} Tbps ({pct_lost}%)",
        f"Network components: {components_before} → {components_after}",
    ]
    if affected_regions:
        summary_lines.append(f"Affected regions: {', '.join(affected_regions)}")

    return SimulationResult(
        scenario_id=scenario_id,
        cable_cuts=cable_cuts,
        cable_names=cable_names,
        total_nodes=n,
        isolated_node_ids=isolated_ids,
        isolated_node_names=isolated_names,
        components_before=components_before,
        components_after=components_after,
        total_pairs=total_pairs,
        disconnected_pairs=disconnected_pairs,
        percent_pairs_disconnected=pct_disconnected,
        total_capacity_tbps=round(total_capacity, 1),
        lost_capacity_tbps=round(lost_capacity, 1),
        percent_capacity_lost=pct_lost,
        affected_regions=affected_regions,
        summary_lines=summary_lines,
    )
