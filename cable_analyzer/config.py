DEMO_MODE = True
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# Risk scoring weights (sum = 100)
CENTRALITY_WEIGHT = 40      # betweenness centrality contribution
CABLE_COUNT_WEIGHT = 30     # number of cables landing (more = higher impact if attacked)
JURISDICTION_WEIGHT = 15    # country risk factor
GEOGRAPHY_WEIGHT = 15       # geographic chokepoint factor

# Jurisdiction risk tiers
HIGH_RISK_COUNTRIES = {"China", "Russia", "Iran", "North Korea", "Yemen", "Syria"}
MEDIUM_RISK_COUNTRIES = {"Pakistan", "Egypt", "Djibouti", "Oman"}

# Geographic chokepoints and their base scores (0-15)
CHOKEPOINT_SCORES: dict[str, int] = {
    "Djibouti": 15,     # Bab el-Mandeb / Red Sea gateway
    "Yemen": 15,        # Bab el-Mandeb
    "Egypt": 12,        # Suez Canal corridor
    "Oman": 10,         # Strait of Hormuz
    "Taiwan": 12,       # Taiwan Strait
    "Singapore": 12,    # Strait of Malacca
    "Malaysia": 8,      # Malacca approach
    "Philippines": 8,   # Luzon Strait
}

# Risk level thresholds
CRITICAL_THRESHOLD = 75
HIGH_THRESHOLD = 50
MEDIUM_THRESHOLD = 25

# Centrality scaling: centrality * CENTRALITY_SCALE, capped at CENTRALITY_WEIGHT
CENTRALITY_SCALE = 500

# Cable count scoring thresholds
CABLE_COUNT_TIERS = [
    (5, 30),   # 5+ cables → 30 pts
    (4, 24),
    (3, 18),
    (2, 10),
    (1, 4),
]

EDGAR_USER_AGENT = "cable-resilience-analyzer/1.0 jak.potvin@gmail.com"
