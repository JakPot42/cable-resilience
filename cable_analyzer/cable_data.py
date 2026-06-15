"""
Curated submarine cable dataset from public sources.
Primary source: TeleGeography Submarine Cable Map (telegeography.com/telecom-resources/submarine-cable-map/)
Landing station coordinates from TeleGeography and ITU public data.
"""

LANDING_POINTS: list[dict] = [
    # North America
    {"id": "LP001", "name": "Virginia Beach", "city": "Virginia Beach", "country": "United States", "region": "North America", "lat": 36.852, "lon": -75.978},
    {"id": "LP002", "name": "Morro Bay", "city": "Morro Bay", "country": "United States", "region": "North America", "lat": 35.367, "lon": -120.850},
    {"id": "LP003", "name": "Hillsboro", "city": "Hillsboro", "country": "United States", "region": "North America", "lat": 45.509, "lon": -122.990},
    {"id": "LP004", "name": "Miami", "city": "Miami", "country": "United States", "region": "North America", "lat": 25.761, "lon": -80.194},
    {"id": "LP005", "name": "Rockaway Beach", "city": "New York", "country": "United States", "region": "North America", "lat": 40.576, "lon": -73.836},
    {"id": "LP006", "name": "Boca Raton", "city": "Boca Raton", "country": "United States", "region": "North America", "lat": 26.369, "lon": -80.107},
    {"id": "LP007", "name": "Fortaleza", "city": "Fortaleza", "country": "Brazil", "region": "South America", "lat": -3.731, "lon": -38.521},
    # Europe
    {"id": "LP010", "name": "Bude", "city": "Bude", "country": "United Kingdom", "region": "Europe", "lat": 50.826, "lon": -4.543},
    {"id": "LP011", "name": "Porthcurno", "city": "Porthcurno", "country": "United Kingdom", "region": "Europe", "lat": 50.046, "lon": -5.704},
    {"id": "LP012", "name": "Sopelana", "city": "Bilbao", "country": "Spain", "region": "Europe", "lat": 43.385, "lon": -2.997},
    {"id": "LP013", "name": "Saint-Hilaire-de-Riez", "city": "Vendée", "country": "France", "region": "Europe", "lat": 46.877, "lon": -2.003},
    {"id": "LP014", "name": "Penmarch", "city": "Brittany", "country": "France", "region": "Europe", "lat": 47.819, "lon": -4.377},
    {"id": "LP015", "name": "Marseille", "city": "Marseille", "country": "France", "region": "Europe", "lat": 43.296, "lon": 5.381},
    {"id": "LP016", "name": "Catania", "city": "Catania", "country": "Italy", "region": "Europe", "lat": 37.502, "lon": 15.091},
    {"id": "LP017", "name": "Laurion", "city": "Athens", "country": "Greece", "region": "Europe", "lat": 37.715, "lon": 24.046},
    {"id": "LP018", "name": "Palermo", "city": "Palermo", "country": "Italy", "region": "Europe", "lat": 38.116, "lon": 13.362},
    # Mediterranean / Middle East
    {"id": "LP020", "name": "Alexandria", "city": "Alexandria", "country": "Egypt", "region": "Middle East / Africa", "lat": 31.200, "lon": 29.919},
    {"id": "LP021", "name": "Port Said", "city": "Port Said", "country": "Egypt", "region": "Middle East / Africa", "lat": 31.256, "lon": 32.289},
    {"id": "LP022", "name": "Djibouti City", "city": "Djibouti City", "country": "Djibouti", "region": "Middle East / Africa", "lat": 11.589, "lon": 43.145},
    {"id": "LP023", "name": "Fujairah", "city": "Fujairah", "country": "United Arab Emirates", "region": "Middle East / Africa", "lat": 25.114, "lon": 56.336},
    {"id": "LP024", "name": "Muscat", "city": "Muscat", "country": "Oman", "region": "Middle East / Africa", "lat": 23.614, "lon": 58.593},
    {"id": "LP025", "name": "Karachi", "city": "Karachi", "country": "Pakistan", "region": "South Asia", "lat": 24.861, "lon": 66.990},
    {"id": "LP026", "name": "Jeddah", "city": "Jeddah", "country": "Saudi Arabia", "region": "Middle East / Africa", "lat": 21.543, "lon": 39.173},
    {"id": "LP027", "name": "Aden", "city": "Aden", "country": "Yemen", "region": "Middle East / Africa", "lat": 12.786, "lon": 44.996},
    # South / Southeast Asia
    {"id": "LP030", "name": "Mumbai", "city": "Mumbai", "country": "India", "region": "South Asia", "lat": 18.891, "lon": 72.804},
    {"id": "LP031", "name": "Chennai", "city": "Chennai", "country": "India", "region": "South Asia", "lat": 13.067, "lon": 80.295},
    {"id": "LP032", "name": "Tuas", "city": "Singapore", "country": "Singapore", "region": "Southeast Asia", "lat": 1.295, "lon": 103.621},
    {"id": "LP033", "name": "Changi", "city": "Singapore", "country": "Singapore", "region": "Southeast Asia", "lat": 1.352, "lon": 104.002},
    {"id": "LP034", "name": "Penang", "city": "Penang", "country": "Malaysia", "region": "Southeast Asia", "lat": 5.417, "lon": 100.343},
    {"id": "LP035", "name": "Batangas", "city": "Batangas", "country": "Philippines", "region": "Southeast Asia", "lat": 13.753, "lon": 121.058},
    {"id": "LP036", "name": "Daet", "city": "Daet", "country": "Philippines", "region": "Southeast Asia", "lat": 14.099, "lon": 122.964},
    {"id": "LP037", "name": "Da Nang", "city": "Da Nang", "country": "Vietnam", "region": "Southeast Asia", "lat": 15.881, "lon": 108.326},
    {"id": "LP038", "name": "Satun", "city": "Satun", "country": "Thailand", "region": "Southeast Asia", "lat": 6.641, "lon": 100.063},
    # East Asia
    {"id": "LP040", "name": "Chikura", "city": "Chikura", "country": "Japan", "region": "East Asia", "lat": 35.060, "lon": 140.208},
    {"id": "LP041", "name": "Miura", "city": "Miura", "country": "Japan", "region": "East Asia", "lat": 35.163, "lon": 139.633},
    {"id": "LP042", "name": "Tanegashima", "city": "Tanegashima", "country": "Japan", "region": "East Asia", "lat": 30.517, "lon": 130.982},
    {"id": "LP043", "name": "Naha", "city": "Okinawa", "country": "Japan", "region": "East Asia", "lat": 26.212, "lon": 127.685},
    {"id": "LP044", "name": "Busan", "city": "Busan", "country": "South Korea", "region": "East Asia", "lat": 35.105, "lon": 129.042},
    {"id": "LP045", "name": "Koje", "city": "Koje", "country": "South Korea", "region": "East Asia", "lat": 34.870, "lon": 128.622},
    {"id": "LP046", "name": "Bali (Taipei)", "city": "Taipei", "country": "Taiwan", "region": "East Asia", "lat": 25.134, "lon": 121.442},
    {"id": "LP047", "name": "Fangshan", "city": "Fangshan", "country": "Taiwan", "region": "East Asia", "lat": 22.018, "lon": 120.677},
    {"id": "LP048", "name": "Shantou", "city": "Shantou", "country": "China", "region": "East Asia", "lat": 23.354, "lon": 116.679},
    {"id": "LP049", "name": "Hong Kong", "city": "Hong Kong", "country": "China", "region": "East Asia", "lat": 22.303, "lon": 114.171},
    {"id": "LP050", "name": "Shanghai", "city": "Shanghai", "country": "China", "region": "East Asia", "lat": 31.231, "lon": 121.474},
    # Pacific
    {"id": "LP060", "name": "Barrigada", "city": "Guam", "country": "United States", "region": "Pacific", "lat": 13.481, "lon": 144.793},
    {"id": "LP061", "name": "Makaha", "city": "Hawaii", "country": "United States", "region": "Pacific", "lat": 21.476, "lon": -158.213},
    {"id": "LP062", "name": "Tafuna", "city": "American Samoa", "country": "United States", "region": "Pacific", "lat": -14.338, "lon": -170.772},
    # Africa
    {"id": "LP070", "name": "Dakar", "city": "Dakar", "country": "Senegal", "region": "Africa", "lat": 14.745, "lon": -17.465},
    {"id": "LP071", "name": "Accra", "city": "Accra", "country": "Ghana", "region": "Africa", "lat": 5.556, "lon": -0.201},
    {"id": "LP072", "name": "Lagos", "city": "Lagos", "country": "Nigeria", "region": "Africa", "lat": 6.453, "lon": 3.396},
    {"id": "LP073", "name": "Mombasa", "city": "Mombasa", "country": "Kenya", "region": "Africa", "lat": -4.046, "lon": 39.663},
    {"id": "LP074", "name": "Cape Town", "city": "Cape Town", "country": "South Africa", "region": "Africa", "lat": -33.913, "lon": 18.418},
]

# Submarine cable dataset.
# path_coords: simplified lat/lon waypoints for map rendering.
# Pacific cables use adjusted longitudes (<-180) to ensure westbound routing in Leaflet.
CABLES: list[dict] = [
    # ─── TRANS-ATLANTIC ───
    {
        "id": "CAB001", "name": "MAREA",
        "landing_point_ids": ["LP001", "LP012"],
        "length_km": 6600, "capacity_tbps": 200.0, "rfs_year": 2017,
        "owners": ["Meta", "Microsoft"], "region": "Trans-Atlantic",
        "path_coords": [(36.852, -75.978), (45.0, -40.0), (43.385, -2.997)],
    },
    {
        "id": "CAB002", "name": "Dunant",
        "landing_point_ids": ["LP001", "LP013"],
        "length_km": 6600, "capacity_tbps": 250.0, "rfs_year": 2021,
        "owners": ["Google"], "region": "Trans-Atlantic",
        "path_coords": [(36.852, -75.978), (47.0, -38.0), (46.877, -2.003)],
    },
    {
        "id": "CAB003", "name": "Grace Hopper",
        "landing_point_ids": ["LP005", "LP010", "LP012"],
        "length_km": 6200, "capacity_tbps": 350.0, "rfs_year": 2022,
        "owners": ["Google"], "region": "Trans-Atlantic",
        "path_coords": [(40.576, -73.836), (50.0, -30.0), (50.826, -4.543), (43.385, -2.997)],
    },
    {
        "id": "CAB004", "name": "Amitié",
        "landing_point_ids": ["LP001", "LP010", "LP014"],
        "length_km": 6800, "capacity_tbps": 400.0, "rfs_year": 2025,
        "owners": ["Meta", "Microsoft", "SFR"], "region": "Trans-Atlantic",
        "path_coords": [(36.852, -75.978), (48.0, -30.0), (50.826, -4.543), (47.819, -4.377)],
    },
    {
        "id": "CAB005", "name": "TAT-14",
        "landing_point_ids": ["LP001", "LP011", "LP015"],
        "length_km": 15428, "capacity_tbps": 3.2, "rfs_year": 2001,
        "owners": ["Multi-owner consortium"], "region": "Trans-Atlantic",
        "path_coords": [(36.852, -75.978), (46.0, -32.0), (50.046, -5.704), (43.296, 5.381)],
    },
    # ─── TRANS-PACIFIC ───
    {
        "id": "CAB006", "name": "FASTER",
        "landing_point_ids": ["LP003", "LP040", "LP042"],
        # Adjusted lons for Pacific: 140.208-360=-219.792, 130.982-360=-229.018
        "length_km": 9000, "capacity_tbps": 60.0, "rfs_year": 2016,
        "owners": ["Google"], "region": "Trans-Pacific",
        "path_coords": [(45.509, -122.990), (40.0, -155.0), (35.060, -219.792), (30.517, -229.018)],
    },
    {
        "id": "CAB007", "name": "JUPITER",
        "landing_point_ids": ["LP002", "LP042", "LP036"],
        # Tanegashima: 130.982-360=-229.018, Daet: 122.964-360=-237.036
        "length_km": 14557, "capacity_tbps": 60.0, "rfs_year": 2020,
        "owners": ["Amazon", "Meta", "SoftBank"], "region": "Trans-Pacific",
        "path_coords": [(35.367, -120.850), (20.0, -165.0), (30.517, -229.018), (14.099, -237.036)],
    },
    {
        "id": "CAB008", "name": "New Cross Pacific (NCP)",
        "landing_point_ids": ["LP003", "LP040", "LP044", "LP046"],
        # Chikura: -219.792, Busan: 129.042-360=-230.958, Taipei: 121.442-360=-238.558
        "length_km": 13618, "capacity_tbps": 80.0, "rfs_year": 2016,
        "owners": ["Multi-owner consortium"], "region": "Trans-Pacific",
        "path_coords": [(45.509, -122.990), (42.0, -155.0), (35.060, -219.792), (35.105, -230.958), (25.134, -238.558)],
    },
    {
        "id": "CAB009", "name": "UNITY",
        "landing_point_ids": ["LP002", "LP041", "LP040"],
        # Miura: 139.633-360=-220.367, Chikura: -219.792
        "length_km": 10000, "capacity_tbps": 7.7, "rfs_year": 2010,
        "owners": ["Google", "SoftBank", "KDDI"], "region": "Trans-Pacific",
        "path_coords": [(35.367, -120.850), (30.0, -158.0), (35.163, -220.367), (35.060, -219.792)],
    },
    # ─── ASIA REGIONAL ───
    {
        "id": "CAB010", "name": "TPE (Trans-Pacific Express)",
        "landing_point_ids": ["LP047", "LP046", "LP043", "LP045", "LP048", "LP032"],
        "length_km": 18000, "capacity_tbps": 5.12, "rfs_year": 2008,
        "owners": ["Multi-owner consortium"], "region": "Asia Regional",
        "path_coords": [(22.018, 120.677), (25.134, 121.442), (26.212, 127.685), (34.870, 128.622), (23.354, 116.679), (1.295, 103.621)],
    },
    {
        "id": "CAB011", "name": "APCN-2",
        "landing_point_ids": ["LP040", "LP044", "LP049", "LP048", "LP032"],
        "length_km": 19000, "capacity_tbps": 2.56, "rfs_year": 2001,
        "owners": ["Multi-owner consortium"], "region": "Asia Regional",
        "path_coords": [(35.060, 140.208), (35.105, 129.042), (22.303, 114.171), (23.354, 116.679), (1.295, 103.621)],
    },
    {
        "id": "CAB012", "name": "AAG (Asia America Gateway)",
        "landing_point_ids": ["LP002", "LP043", "LP049", "LP037", "LP034", "LP032"],
        # Okinawa adjusted for Pacific crossing from US: 127.685-360=-232.315
        "length_km": 20000, "capacity_tbps": 40.0, "rfs_year": 2009,
        "owners": ["Multi-owner consortium"], "region": "Trans-Pacific",
        "path_coords": [(35.367, -120.850), (20.0, -170.0), (26.212, -232.315), (22.303, 114.171), (15.881, 108.326), (5.417, 100.343), (1.295, 103.621)],
    },
    # ─── ASIA-EUROPE (Critical chokepoints: Egypt, Djibouti, Singapore) ───
    {
        "id": "CAB013", "name": "SEA-ME-WE 3",
        "landing_point_ids": ["LP010", "LP015", "LP020", "LP022", "LP031", "LP032"],
        "length_km": 39000, "capacity_tbps": 2.56, "rfs_year": 1999,
        "owners": ["Multi-owner consortium"], "region": "Asia-Europe",
        "path_coords": [(50.826, -4.543), (43.296, 5.381), (31.200, 29.919), (11.589, 43.145), (13.067, 80.295), (1.295, 103.621)],
    },
    {
        "id": "CAB014", "name": "SEA-ME-WE 5",
        "landing_point_ids": ["LP010", "LP015", "LP020", "LP022", "LP025", "LP031", "LP032"],
        "length_km": 20000, "capacity_tbps": 24.0, "rfs_year": 2016,
        "owners": ["Multi-owner consortium"], "region": "Asia-Europe",
        "path_coords": [(50.826, -4.543), (43.296, 5.381), (31.200, 29.919), (11.589, 43.145), (24.861, 66.990), (13.067, 80.295), (1.295, 103.621)],
    },
    {
        "id": "CAB015", "name": "AAE-1 (Asia Africa Europe 1)",
        "landing_point_ids": ["LP049", "LP032", "LP031", "LP025", "LP023", "LP022", "LP020", "LP016", "LP017"],
        "length_km": 25000, "capacity_tbps": 40.0, "rfs_year": 2017,
        "owners": ["Multi-owner consortium"], "region": "Asia-Europe",
        "path_coords": [(22.303, 114.171), (1.295, 103.621), (13.067, 80.295), (24.861, 66.990), (25.114, 56.336), (11.589, 43.145), (31.200, 29.919), (37.502, 15.091), (37.715, 24.046)],
    },
    {
        "id": "CAB016", "name": "EIG (Europe India Gateway)",
        "landing_point_ids": ["LP010", "LP012", "LP015", "LP020", "LP023", "LP031"],
        "length_km": 15000, "capacity_tbps": 3.84, "rfs_year": 2012,
        "owners": ["Multi-owner consortium"], "region": "Asia-Europe",
        "path_coords": [(50.826, -4.543), (43.385, -2.997), (43.296, 5.381), (31.200, 29.919), (25.114, 56.336), (13.067, 80.295)],
    },
    # ─── AFRICA ───
    {
        "id": "CAB017", "name": "EASSy (Eastern Africa Submarine System)",
        "landing_point_ids": ["LP074", "LP073", "LP022", "LP020", "LP016", "LP010"],
        "length_km": 10500, "capacity_tbps": 3.84, "rfs_year": 2010,
        "owners": ["Multi-owner consortium"], "region": "Africa-Europe",
        "path_coords": [(-33.913, 18.418), (-4.046, 39.663), (11.589, 43.145), (31.200, 29.919), (37.502, 15.091), (50.826, -4.543)],
    },
    {
        "id": "CAB018", "name": "WACS (West Africa Cable System)",
        "landing_point_ids": ["LP010", "LP070", "LP071", "LP072", "LP074"],
        "length_km": 14900, "capacity_tbps": 5.12, "rfs_year": 2012,
        "owners": ["Multi-owner consortium"], "region": "Africa-Europe",
        "path_coords": [(50.826, -4.543), (14.745, -17.465), (5.556, -0.201), (6.453, 3.396), (-33.913, 18.418)],
    },
    {
        "id": "CAB019", "name": "South Atlantic Cable System (SACS)",
        "landing_point_ids": ["LP001", "LP007", "LP074"],
        "length_km": 12000, "capacity_tbps": 40.0, "rfs_year": 2018,
        "owners": ["Angola Cables", "ANATEL"], "region": "Trans-Atlantic",
        "path_coords": [(36.852, -75.978), (-3.731, -38.521), (-33.913, 18.418)],
    },
    {
        "id": "CAB020", "name": "PEACE (Pakistan & East Africa Connecting Europe)",
        "landing_point_ids": ["LP025", "LP023", "LP022", "LP073", "LP074"],
        "length_km": 12000, "capacity_tbps": 96.0, "rfs_year": 2024,
        "owners": ["PEACE Cable International Network"], "region": "Asia-Africa",
        "path_coords": [(24.861, 66.990), (25.114, 56.336), (11.589, 43.145), (-4.046, 39.663), (-33.913, 18.418)],
    },
]

# Quick lookup helpers
LANDING_POINT_BY_ID: dict[str, dict] = {lp["id"]: lp for lp in LANDING_POINTS}
CABLE_BY_ID: dict[str, dict] = {c["id"]: c for c in CABLES}
