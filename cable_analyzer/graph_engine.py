from __future__ import annotations

import networkx as nx

from .cable_data import CABLES, LANDING_POINTS, CABLE_BY_ID


def build_graph(
    cables: list[dict] | None = None,
    landing_points: list[dict] | None = None,
) -> nx.Graph:
    """
    Build undirected weighted graph. Nodes = landing stations, edges = cables.
    Only landing stations that appear in at least one cable are included as nodes;
    stations in LANDING_POINTS but with no cable are shown on the map but omitted
    from graph analysis to keep the network connected and the betweenness centrality
    meaningful.
    """
    if cables is None:
        cables = CABLES
    if landing_points is None:
        landing_points = LANDING_POINTS

    # Only include LP IDs that appear in at least one cable
    connected_lp_ids: set[str] = set()
    for cable in cables:
        for lp_id in cable["landing_point_ids"]:
            connected_lp_ids.add(lp_id)

    lp_by_id = {lp["id"]: lp for lp in landing_points}

    G = nx.Graph()
    for lp_id in connected_lp_ids:
        lp = lp_by_id.get(lp_id)
        if lp:
            G.add_node(lp_id, **lp)

    for cable in cables:
        lp_ids = cable["landing_point_ids"]
        for i in range(len(lp_ids) - 1):
            u, v = lp_ids[i], lp_ids[i + 1]
            # Normalize edge direction so (u,v) and (v,u) are the same
            u, v = min(u, v), max(u, v)
            if G.has_edge(u, v):
                G[u][v]["cable_ids"].append(cable["id"])
                G[u][v]["capacity_tbps"] += cable.get("capacity_tbps", 0.0)
            else:
                G.add_edge(
                    u, v,
                    cable_ids=[cable["id"]],
                    capacity_tbps=cable.get("capacity_tbps", 0.0),
                    length_km=cable.get("length_km", 0),
                )
    return G


def compute_betweenness_centrality(G: nx.Graph) -> dict[str, float]:
    """
    Betweenness centrality weighted by inverse capacity.
    High-capacity routes are "preferred" paths (lower effective weight).
    """
    for u, v in G.edges():
        cap = G[u][v].get("capacity_tbps", 1.0)
        G[u][v]["weight"] = 1.0 / cap if cap > 0 else 999.0
    return nx.betweenness_centrality(G, weight="weight", normalized=True)


def cable_counts_per_station(
    cables: list[dict] | None = None,
    landing_points: list[dict] | None = None,
) -> dict[str, int]:
    """Return {lp_id: number_of_unique_cables_landing_here}."""
    if cables is None:
        cables = CABLES
    if landing_points is None:
        landing_points = LANDING_POINTS

    counts: dict[str, int] = {lp["id"]: 0 for lp in landing_points}
    for cable in cables:
        for lp_id in cable["landing_point_ids"]:
            if lp_id in counts:
                counts[lp_id] += 1
    return counts


def get_cables_for_station(lp_id: str, cables: list[dict] | None = None) -> list[dict]:
    """Return all cable objects whose route includes lp_id."""
    if cables is None:
        cables = CABLES
    return [c for c in cables if lp_id in c["landing_point_ids"]]


def total_capacity_for_station(lp_id: str, cables: list[dict] | None = None) -> float:
    """Sum of capacity_tbps across all cables landing at a station."""
    return sum(
        c.get("capacity_tbps", 0.0)
        for c in get_cables_for_station(lp_id, cables)
    )


def is_graph_connected(G: nx.Graph) -> bool:
    return nx.is_connected(G)


def top_chokepoints(
    centrality: dict[str, float],
    risk_scores: dict[str, dict],
    n: int = 10,
) -> list[dict]:
    """Return top-n landing stations sorted by centrality descending."""
    from .cable_data import LANDING_POINT_BY_ID

    ranked = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    result = []
    for lp_id, score in ranked[:n]:
        lp = LANDING_POINT_BY_ID.get(lp_id, {})
        result.append({
            "lp_id": lp_id,
            "name": lp.get("name", lp_id),
            "country": lp.get("country", ""),
            "region": lp.get("region", ""),
            "centrality": round(score, 4),
            "risk_level": risk_scores.get(lp_id, {}).get("level", "LOW"),
            "risk_score": risk_scores.get(lp_id, {}).get("score", 0),
        })
    return result
