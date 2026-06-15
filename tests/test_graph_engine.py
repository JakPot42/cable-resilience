import pytest
import networkx as nx
from cable_analyzer.cable_data import CABLES, LANDING_POINTS
from cable_analyzer.graph_engine import (
    build_graph,
    compute_betweenness_centrality,
    cable_counts_per_station,
    get_cables_for_station,
    total_capacity_for_station,
    is_graph_connected,
)


@pytest.fixture(scope="module")
def G():
    return build_graph(CABLES, LANDING_POINTS)


@pytest.fixture(scope="module")
def centrality(G):
    return compute_betweenness_centrality(G)


class TestBuildGraph:
    def test_node_count_matches_connected_landing_points(self, G):
        # Only LPs that appear in at least one cable are graph nodes
        connected_ids = set()
        for c in CABLES:
            connected_ids.update(c["landing_point_ids"])
        assert G.number_of_nodes() == len(connected_ids)

    def test_has_edges(self, G):
        assert G.number_of_edges() > 0

    def test_nodes_have_lat_lon(self, G):
        for node, data in G.nodes(data=True):
            assert "lat" in data and "lon" in data

    def test_edges_have_cable_ids(self, G):
        for u, v, data in G.edges(data=True):
            assert "cable_ids" in data
            assert len(data["cable_ids"]) >= 1

    def test_edges_have_capacity(self, G):
        for u, v, data in G.edges(data=True):
            assert data.get("capacity_tbps", 0) > 0

    def test_all_cable_landing_point_ids_are_nodes(self, G):
        # Every LP referenced in a cable must be in the graph
        for cable in CABLES:
            for lp_id in cable["landing_point_ids"]:
                assert lp_id in G.nodes, f"{lp_id} missing from graph"

    def test_graph_is_connected(self, G):
        assert is_graph_connected(G)


class TestBetweennessCentrality:
    def test_returns_all_nodes(self, G, centrality):
        assert set(centrality.keys()) == set(G.nodes())

    def test_values_between_0_and_1(self, centrality):
        for val in centrality.values():
            assert 0.0 <= val <= 1.0

    def test_singapore_has_nonzero_centrality(self, centrality):
        # Singapore (LP032) is a major hub — should have measurable centrality
        assert centrality.get("LP032", 0) > 0

    def test_djibouti_has_nonzero_centrality(self, centrality):
        assert centrality.get("LP022", 0) > 0

    def test_hub_outranks_leaf(self, centrality):
        # Singapore should outrank a peripheral Pacific node
        sg = centrality.get("LP032", 0)
        guam = centrality.get("LP060", 0)
        assert sg > guam


class TestCableCounts:
    def test_returns_all_stations(self):
        counts = cable_counts_per_station(CABLES, LANDING_POINTS)
        assert set(counts.keys()) == {lp["id"] for lp in LANDING_POINTS}

    def test_singapore_has_multiple_cables(self):
        counts = cable_counts_per_station(CABLES, LANDING_POINTS)
        assert counts.get("LP032", 0) >= 3

    def test_count_nonnegative(self):
        counts = cable_counts_per_station(CABLES, LANDING_POINTS)
        for count in counts.values():
            assert count >= 0


class TestHelpers:
    def test_get_cables_for_station_returns_list(self):
        result = get_cables_for_station("LP032", CABLES)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_cables_for_unknown_station(self):
        result = get_cables_for_station("LP999", CABLES)
        assert result == []

    def test_total_capacity_positive_for_hub(self):
        cap = total_capacity_for_station("LP032", CABLES)
        assert cap > 0

    def test_total_capacity_zero_for_unknown(self):
        cap = total_capacity_for_station("LP999", CABLES)
        assert cap == 0.0
