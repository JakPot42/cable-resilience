import pytest
from cable_analyzer.cable_data import CABLES, LANDING_POINTS
from cable_analyzer.graph_engine import build_graph
from cable_analyzer.simulation import run_simulation, SimulationResult


@pytest.fixture(scope="module")
def G():
    return build_graph(CABLES, LANDING_POINTS)


class TestRunSimulation:
    def test_returns_simulation_result(self, G):
        result = run_simulation(["CAB001"], G=G)
        assert isinstance(result, SimulationResult)

    def test_cable_cut_names_populated(self, G):
        result = run_simulation(["CAB001"], G=G)
        assert "MAREA" in result.cable_names

    def test_total_nodes_equals_connected_landing_points(self, G):
        # Graph only contains LPs that appear in at least one cable
        result = run_simulation(["CAB001"], G=G)
        assert result.total_nodes == G.number_of_nodes()

    def test_capacity_lost_is_non_negative(self, G):
        result = run_simulation(["CAB001"], G=G)
        assert result.lost_capacity_tbps >= 0

    def test_total_capacity_is_positive(self, G):
        result = run_simulation(["CAB001"], G=G)
        assert result.total_capacity_tbps > 0

    def test_capacity_lost_does_not_exceed_total(self, G):
        result = run_simulation(["CAB001"], G=G)
        assert result.lost_capacity_tbps <= result.total_capacity_tbps

    def test_percent_disconnected_in_range(self, G):
        result = run_simulation(["CAB001"], G=G)
        assert 0.0 <= result.percent_pairs_disconnected <= 100.0

    def test_components_after_gte_before_or_equal(self, G):
        result = run_simulation(["CAB001"], G=G)
        assert result.components_after >= result.components_before

    def test_summary_lines_populated(self, G):
        result = run_simulation(["CAB001"], G=G)
        assert len(result.summary_lines) >= 3

    def test_scenario_id_stored(self, G):
        result = run_simulation(["CAB001"], scenario_id="test-id", G=G)
        assert result.scenario_id == "test-id"

    def test_taiwan_strait_n2_isolates_taiwan(self, G):
        # Cutting TPE and NCP should isolate or degrade Taiwan LP046 and LP047
        result = run_simulation(["CAB010", "CAB008"], scenario_id="taiwan-strait", G=G)
        # Taiwan stations should be isolated (no other cables connect them)
        assert "LP046" in result.isolated_node_ids or "LP047" in result.isolated_node_ids

    def test_n2_more_impactful_than_n1_for_same_cable_set(self, G):
        n1 = run_simulation(["CAB014"], G=G)
        n2 = run_simulation(["CAB014", "CAB015"], G=G)
        assert n2.lost_capacity_tbps >= n1.lost_capacity_tbps

    def test_empty_cut_list_no_impact(self, G):
        result = run_simulation([], G=G)
        assert result.lost_capacity_tbps == 0.0
        assert result.isolated_node_ids == []
        assert result.components_after == result.components_before
