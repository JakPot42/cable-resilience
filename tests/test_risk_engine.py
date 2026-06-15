import pytest
from cable_analyzer.risk_engine import score_landing_station, score_all_stations
from cable_analyzer.cable_data import LANDING_POINTS
from cable_analyzer.graph_engine import build_graph, compute_betweenness_centrality, cable_counts_per_station
from cable_analyzer.cable_data import CABLES


REQUIRED_KEYS = {"score", "level", "components"}
REQUIRED_COMPONENT_KEYS = {"centrality", "cable_count", "jurisdiction", "geography"}


@pytest.fixture(scope="module")
def centrality():
    G = build_graph(CABLES, LANDING_POINTS)
    return compute_betweenness_centrality(G)


@pytest.fixture(scope="module")
def counts():
    return cable_counts_per_station(CABLES, LANDING_POINTS)


class TestScoreLandingStation:
    def test_returns_required_keys(self):
        lp = {"id": "LP001", "country": "United States", "region": "North America"}
        result = score_landing_station(lp, 0.05, 3)
        assert REQUIRED_KEYS.issubset(result.keys())

    def test_components_have_required_keys(self):
        lp = {"id": "LP001", "country": "United States", "region": "North America"}
        result = score_landing_station(lp, 0.05, 3)
        assert REQUIRED_COMPONENT_KEYS.issubset(result["components"].keys())

    def test_zero_centrality_gives_zero_centrality_score(self):
        lp = {"id": "LP001", "country": "United States", "region": "North America"}
        result = score_landing_station(lp, 0.0, 1)
        assert result["components"]["centrality"] == 0.0

    def test_high_centrality_capped_at_40(self):
        lp = {"id": "LP001", "country": "United States", "region": "North America"}
        result = score_landing_station(lp, 1.0, 1)
        assert result["components"]["centrality"] <= 40.0

    def test_five_plus_cables_gives_max_cable_score(self):
        lp = {"id": "LP001", "country": "United States", "region": "North America"}
        result = score_landing_station(lp, 0.0, 6)
        assert result["components"]["cable_count"] == 30

    def test_single_cable_gives_lowest_cable_score(self):
        lp = {"id": "LP001", "country": "United States", "region": "North America"}
        result = score_landing_station(lp, 0.0, 1)
        assert result["components"]["cable_count"] == 4

    def test_high_risk_country_adds_jurisdiction_score(self):
        lp = {"id": "LP027", "country": "Yemen", "region": "Middle East / Africa"}
        result = score_landing_station(lp, 0.0, 1)
        assert result["components"]["jurisdiction"] == 15

    def test_medium_risk_country_adds_partial_jurisdiction(self):
        lp = {"id": "LP022", "country": "Djibouti", "region": "Middle East / Africa"}
        result = score_landing_station(lp, 0.0, 1)
        assert result["components"]["jurisdiction"] == 8

    def test_low_risk_country_zero_jurisdiction(self):
        lp = {"id": "LP001", "country": "United States", "region": "North America"}
        result = score_landing_station(lp, 0.0, 1)
        assert result["components"]["jurisdiction"] == 0

    def test_chokepoint_country_adds_geography_score(self):
        lp = {"id": "LP022", "country": "Djibouti", "region": "Middle East / Africa"}
        result = score_landing_station(lp, 0.0, 1)
        assert result["components"]["geography"] > 0

    def test_non_chokepoint_zero_geography(self):
        lp = {"id": "LP001", "country": "United States", "region": "North America"}
        result = score_landing_station(lp, 0.0, 1)
        assert result["components"]["geography"] == 0

    def test_score_capped_at_100(self):
        lp = {"id": "LP022", "country": "Djibouti", "region": "Middle East / Africa"}
        result = score_landing_station(lp, 1.0, 10)
        assert result["score"] <= 100

    def test_level_critical_at_75(self):
        lp = {"id": "LP022", "country": "Yemen", "region": "Middle East / Africa"}
        result = score_landing_station(lp, 0.5, 6)
        assert result["level"] == "CRITICAL"

    def test_level_low_at_zero(self):
        lp = {"id": "LP001", "country": "United States", "region": "North America"}
        result = score_landing_station(lp, 0.0, 0)
        assert result["level"] == "LOW"


class TestScoreAllStations:
    def test_returns_all_landing_point_ids(self, centrality, counts):
        scores = score_all_stations(LANDING_POINTS, centrality, counts)
        assert set(scores.keys()) == {lp["id"] for lp in LANDING_POINTS}

    def test_singapore_scores_high_or_critical(self, centrality, counts):
        scores = score_all_stations(LANDING_POINTS, centrality, counts)
        sg_level = scores["LP032"]["level"]
        assert sg_level in ("HIGH", "CRITICAL")

    def test_djibouti_scores_high_or_critical(self, centrality, counts):
        scores = score_all_stations(LANDING_POINTS, centrality, counts)
        dj_level = scores["LP022"]["level"]
        assert dj_level in ("HIGH", "CRITICAL")

    def test_all_scores_have_required_keys(self, centrality, counts):
        scores = score_all_stations(LANDING_POINTS, centrality, counts)
        for lp_id, s in scores.items():
            assert REQUIRED_KEYS.issubset(s.keys()), f"Missing keys for {lp_id}"
