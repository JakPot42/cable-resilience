from __future__ import annotations

from .config import (
    CENTRALITY_WEIGHT,
    CENTRALITY_SCALE,
    CABLE_COUNT_TIERS,
    HIGH_RISK_COUNTRIES,
    MEDIUM_RISK_COUNTRIES,
    CHOKEPOINT_SCORES,
    CRITICAL_THRESHOLD,
    HIGH_THRESHOLD,
    MEDIUM_THRESHOLD,
)


def _cable_count_score(count: int) -> int:
    for threshold, score in CABLE_COUNT_TIERS:
        if count >= threshold:
            return score
    return 0


def _level(score: float) -> str:
    if score >= CRITICAL_THRESHOLD:
        return "CRITICAL"
    if score >= HIGH_THRESHOLD:
        return "HIGH"
    if score >= MEDIUM_THRESHOLD:
        return "MEDIUM"
    return "LOW"


def score_landing_station(
    lp: dict,
    centrality_value: float,
    cable_count: int,
) -> dict:
    """
    Score a landing station 0–100 for strategic criticality.
    Higher score = higher impact if this station is attacked / destroyed.

    Components
    ----------
    centrality  : betweenness centrality contribution (0–40 pts)
    cable_count : number of cables landing here (0–30 pts)
    jurisdiction: country geopolitical risk (0–15 pts)
    geography   : chokepoint geography factor (0–15 pts)
    """
    # Betweenness centrality (0–40)
    c_score = min(float(CENTRALITY_WEIGHT), centrality_value * CENTRALITY_SCALE)

    # Cable count — more cables = higher criticality if station is destroyed (0–30)
    cc_score = float(_cable_count_score(cable_count))

    # Jurisdiction risk (0–15)
    country = lp.get("country", "")
    if country in HIGH_RISK_COUNTRIES:
        j_score = 15.0
    elif country in MEDIUM_RISK_COUNTRIES:
        j_score = 8.0
    else:
        j_score = 0.0

    # Chokepoint geography (0–15)
    g_score = float(CHOKEPOINT_SCORES.get(country, 0))

    total = min(100.0, c_score + cc_score + j_score + g_score)
    return {
        "score": round(total),
        "level": _level(total),
        "components": {
            "centrality": round(c_score, 1),
            "cable_count": int(cc_score),
            "jurisdiction": int(j_score),
            "geography": int(g_score),
        },
    }


def score_all_stations(
    landing_points: list[dict],
    centrality: dict[str, float],
    cable_counts: dict[str, int],
) -> dict[str, dict]:
    """Return {lp_id: score_dict} for every landing station."""
    return {
        lp["id"]: score_landing_station(
            lp,
            centrality.get(lp["id"], 0.0),
            cable_counts.get(lp["id"], 0),
        )
        for lp in landing_points
    }
