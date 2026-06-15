import pytest
from cable_analyzer.seed_data import DEMO_SCENARIOS, DEMO_SCENARIO_BY_ID
from cable_analyzer.cable_data import CABLE_BY_ID


REQUIRED_FIELDS = {"id", "name", "description", "cable_cuts", "type",
                   "threat_actor", "nuwc_relevance", "pre_baked_brief"}


class TestDemoScenarios:
    def test_scenarios_not_empty(self):
        assert len(DEMO_SCENARIOS) > 0

    def test_all_have_required_fields(self):
        for s in DEMO_SCENARIOS:
            for field in REQUIRED_FIELDS:
                assert field in s, f"Scenario '{s.get('id')}' missing field '{field}'"

    def test_taiwan_strait_scenario_exists(self):
        assert "taiwan-strait" in DEMO_SCENARIO_BY_ID

    def test_red_sea_scenario_exists(self):
        assert "red-sea" in DEMO_SCENARIO_BY_ID

    def test_singapore_hub_scenario_exists(self):
        assert "singapore-hub" in DEMO_SCENARIO_BY_ID

    def test_cable_ids_reference_valid_cables(self):
        for s in DEMO_SCENARIOS:
            for cid in s["cable_cuts"]:
                assert cid in CABLE_BY_ID, (
                    f"Scenario '{s['id']}' references unknown cable '{cid}'"
                )

    def test_each_scenario_has_at_least_one_cable_cut(self):
        for s in DEMO_SCENARIOS:
            assert len(s["cable_cuts"]) >= 1

    def test_pre_baked_briefs_are_nonempty(self):
        for s in DEMO_SCENARIOS:
            assert len(s["pre_baked_brief"]) > 50, (
                f"Scenario '{s['id']}' has too-short brief"
            )

    def test_by_id_lookup_works(self):
        for s in DEMO_SCENARIOS:
            assert DEMO_SCENARIO_BY_ID[s["id"]] is s

    def test_scenario_ids_are_unique(self):
        ids = [s["id"] for s in DEMO_SCENARIOS]
        assert len(ids) == len(set(ids))

    def test_taiwan_strait_cuts_tpe_and_ncp(self):
        s = DEMO_SCENARIO_BY_ID["taiwan-strait"]
        assert "CAB010" in s["cable_cuts"]  # TPE
        assert "CAB008" in s["cable_cuts"]  # NCP

    def test_red_sea_cuts_smw5_and_aae1(self):
        s = DEMO_SCENARIO_BY_ID["red-sea"]
        assert "CAB014" in s["cable_cuts"]  # SEA-ME-WE 5
        assert "CAB015" in s["cable_cuts"]  # AAE-1
