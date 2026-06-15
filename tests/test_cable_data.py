import pytest
from cable_analyzer.cable_data import CABLES, LANDING_POINTS, CABLE_BY_ID, LANDING_POINT_BY_ID


class TestLandingPoints:
    REQUIRED_FIELDS = {"id", "name", "city", "country", "region", "lat", "lon"}

    def test_landing_points_not_empty(self):
        assert len(LANDING_POINTS) > 0

    def test_all_have_required_fields(self):
        for lp in LANDING_POINTS:
            for field in self.REQUIRED_FIELDS:
                assert field in lp, f"LP {lp.get('id')} missing field '{field}'"

    def test_ids_are_unique(self):
        ids = [lp["id"] for lp in LANDING_POINTS]
        assert len(ids) == len(set(ids))

    def test_lat_in_valid_range(self):
        for lp in LANDING_POINTS:
            assert -90.0 <= lp["lat"] <= 90.0, f"{lp['id']} lat {lp['lat']} out of range"

    def test_lon_in_valid_range(self):
        for lp in LANDING_POINTS:
            assert -180.0 <= lp["lon"] <= 180.0, f"{lp['id']} lon {lp['lon']} out of range"

    def test_by_id_lookup(self):
        for lp in LANDING_POINTS:
            assert LANDING_POINT_BY_ID[lp["id"]] == lp

    def test_regions_are_strings(self):
        for lp in LANDING_POINTS:
            assert isinstance(lp["region"], str) and len(lp["region"]) > 0


class TestCables:
    REQUIRED_FIELDS = {"id", "name", "landing_point_ids", "length_km", "capacity_tbps",
                       "rfs_year", "owners", "region"}

    def test_cables_not_empty(self):
        assert len(CABLES) > 0

    def test_all_have_required_fields(self):
        for cable in CABLES:
            for field in self.REQUIRED_FIELDS:
                assert field in cable, f"Cable {cable.get('id')} missing '{field}'"

    def test_ids_are_unique(self):
        ids = [c["id"] for c in CABLES]
        assert len(ids) == len(set(ids))

    def test_landing_points_reference_valid_ids(self):
        valid_ids = {lp["id"] for lp in LANDING_POINTS}
        for cable in CABLES:
            for lp_id in cable["landing_point_ids"]:
                assert lp_id in valid_ids, (
                    f"Cable {cable['id']} references unknown LP '{lp_id}'"
                )

    def test_each_cable_has_at_least_two_landing_points(self):
        for cable in CABLES:
            assert len(cable["landing_point_ids"]) >= 2, (
                f"Cable {cable['id']} has fewer than 2 landing points"
            )

    def test_capacity_is_positive(self):
        for cable in CABLES:
            assert cable["capacity_tbps"] > 0, f"Cable {cable['id']} has non-positive capacity"

    def test_length_is_positive(self):
        for cable in CABLES:
            assert cable["length_km"] > 0, f"Cable {cable['id']} has non-positive length"

    def test_by_id_lookup(self):
        for cable in CABLES:
            assert CABLE_BY_ID[cable["id"]] == cable

    def test_path_coords_when_present(self):
        for cable in CABLES:
            coords = cable.get("path_coords", [])
            if coords:
                assert len(coords) >= 2, f"Cable {cable['id']} path_coords too short"
                for pt in coords:
                    assert len(pt) == 2, f"Cable {cable['id']} coord not (lat, lon) pair"
