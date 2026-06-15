import pytest
from cable_analyzer.cable_data import CABLES, LANDING_POINTS
from cable_analyzer.graph_engine import (
    build_graph, compute_betweenness_centrality, cable_counts_per_station,
)
from cable_analyzer.risk_engine import score_all_stations
from cable_analyzer.map_generator import generate_global_map, generate_scenario_map


@pytest.fixture(scope="module")
def map_fixtures():
    G = build_graph(CABLES, LANDING_POINTS)
    centrality = compute_betweenness_centrality(G)
    counts = cable_counts_per_station(CABLES, LANDING_POINTS)
    risk_scores = score_all_stations(LANDING_POINTS, centrality, counts)
    return G, risk_scores


class TestGlobalMap:
    def test_returns_string(self, map_fixtures):
        G, risk_scores = map_fixtures
        result = generate_global_map(G, LANDING_POINTS, CABLES, risk_scores)
        assert isinstance(result, str)

    def test_not_empty(self, map_fixtures):
        G, risk_scores = map_fixtures
        result = generate_global_map(G, LANDING_POINTS, CABLES, risk_scores)
        assert len(result) > 1000

    def test_contains_html_tag(self, map_fixtures):
        G, risk_scores = map_fixtures
        result = generate_global_map(G, LANDING_POINTS, CABLES, risk_scores)
        assert "<html" in result.lower()

    def test_contains_leaflet(self, map_fixtures):
        G, risk_scores = map_fixtures
        result = generate_global_map(G, LANDING_POINTS, CABLES, risk_scores)
        assert "leaflet" in result.lower()

    def test_contains_map_element(self, map_fixtures):
        G, risk_scores = map_fixtures
        result = generate_global_map(G, LANDING_POINTS, CABLES, risk_scores)
        assert "CircleMarker" in result or "circle" in result.lower()


class TestScenarioMap:
    def test_returns_string(self, map_fixtures):
        _, risk_scores = map_fixtures
        result = generate_scenario_map(
            LANDING_POINTS, CABLES,
            cut_cable_ids=["CAB014"],
            isolated_lp_ids=["LP046"],
            risk_scores=risk_scores,
        )
        assert isinstance(result, str)

    def test_contains_html_tag(self, map_fixtures):
        _, risk_scores = map_fixtures
        result = generate_scenario_map(
            LANDING_POINTS, CABLES,
            cut_cable_ids=["CAB014"],
            isolated_lp_ids=[],
            risk_scores=risk_scores,
        )
        assert "<html" in result.lower()

    def test_not_empty(self, map_fixtures):
        _, risk_scores = map_fixtures
        result = generate_scenario_map(
            LANDING_POINTS, CABLES,
            cut_cable_ids=[],
            isolated_lp_ids=[],
            risk_scores=risk_scores,
        )
        assert len(result) > 1000

    def test_empty_cut_list_renders(self, map_fixtures):
        _, risk_scores = map_fixtures
        result = generate_scenario_map(
            LANDING_POINTS, CABLES,
            cut_cable_ids=[],
            isolated_lp_ids=[],
            risk_scores=risk_scores,
        )
        assert isinstance(result, str)
