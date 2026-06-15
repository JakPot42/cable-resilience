"""
Pre-defined demonstration scenarios. The simulation results are computed at
startup by running run_simulation() against the graph — not hardcoded here.
"""

DEMO_SCENARIOS: list[dict] = [
    {
        "id": "taiwan-strait",
        "name": "Taiwan Strait Severance (N-2)",
        "description": (
            "Simulates coordinated severance of the two major submarine cable systems "
            "directly connecting Taiwan to the global internet — TPE and NCP — "
            "representing a conflict scenario in the Taiwan Strait."
        ),
        "cable_cuts": ["CAB010", "CAB008"],  # TPE, NCP
        "type": "N-2",
        "threat_actor": "State Actor",
        "nuwc_relevance": (
            "Undersea infrastructure protection in contested waters; cable route assessment "
            "for the Taiwan Strait. Relevant to USN/NUWC undersea domain awareness programs."
        ),
        "pre_baked_brief": (
            "The N-2 severance of TPE and NCP cables isolates Taiwan's primary Pacific "
            "connections. Taiwan (Bali and Fangshan landing stations) loses direct connectivity "
            "to Japan, South Korea, and the United States west coast. Residual connectivity "
            "via Hong Kong and Singapore remains degraded. From a strategic standpoint, "
            "this scenario replicates the communications disruption pattern observed in "
            "historical undersea cable interference events near contested maritime zones. "
            "The DoD and CISA identify trans-Pacific cable concentration as a tier-1 "
            "undersea infrastructure vulnerability. Restoration timelines for transpacific "
            "cable cuts typically range from 2–6 weeks, depending on cable ship availability "
            "and permission to enter contested exclusive economic zones."
        ),
    },
    {
        "id": "red-sea",
        "name": "Red Sea Corridor Disruption (N-2)",
        "description": (
            "Simulates severance of SEA-ME-WE 5 and AAE-1 in the Red Sea corridor, "
            "modeled after the 2024 Houthi attacks on submarine cable infrastructure "
            "that disrupted 25% of Europe-Asia internet traffic."
        ),
        "cable_cuts": ["CAB014", "CAB015"],  # SMW-5, AAE-1
        "type": "N-2",
        "threat_actor": "Non-State Actor / Proxy",
        "nuwc_relevance": (
            "Undersea domain awareness in the Bab el-Mandeb strait; threat assessment "
            "for non-kinetic infrastructure attacks in contested maritime space. "
            "Directly relevant to NAVCENT / 5th Fleet theater undersea operations."
        ),
        "pre_baked_brief": (
            "Simultaneous severance of SEA-ME-WE 5 and AAE-1 removes two of the highest-"
            "capacity routes linking Southeast Asia to Europe through the Red Sea / Suez "
            "corridor. Djibouti (LP022) becomes a partial chokepoint; residual traffic "
            "must reroute via the Cape of Good Hope or through Pacific cables and US "
            "transit — adding 80–120ms of latency. The 2024 Houthi cable attack (modeled "
            "here) disrupted over 25% of Asia-Europe bandwidth and demonstrated that "
            "non-state actors with Iranian proxy support can execute credible undersea "
            "infrastructure attacks. CISA's 2023 National Infrastructure Protection Plan "
            "identifies this corridor as a Tier-1 critical submarine cable risk zone."
        ),
    },
    {
        "id": "singapore-hub",
        "name": "Singapore Hub Failure (N-3)",
        "description": (
            "Simulates simultaneous failure of three major cable systems terminating at "
            "Singapore (TPE, APCN-2, AAG) — representing a hub-and-spoke chokepoint "
            "failure at the Strait of Malacca gateway."
        ),
        "cable_cuts": ["CAB010", "CAB011", "CAB012"],  # TPE, APCN-2, AAG
        "type": "N-3",
        "threat_actor": "Natural Disaster / Coordinated Attack",
        "nuwc_relevance": (
            "Hub-and-spoke vulnerability analysis; maritime chokepoint resilience in "
            "the Strait of Malacca. Singapore ranks among the top three globally critical "
            "submarine cable hubs by betweenness centrality."
        ),
        "pre_baked_brief": (
            "Singapore's Tuas cable landing station hosts or terminates six of the "
            "twenty cables in this dataset. Simultaneous loss of TPE, APCN-2, and AAG "
            "removes major intra-Asian and trans-Pacific routing options. Singapore "
            "itself retains connectivity via SEA-ME-WE 3 and 5 and AAE-1, but its "
            "role as a relay hub for East Asian traffic is severely degraded. This "
            "scenario illustrates why network topology concentration at single "
            "geographic hubs — even highly-redundant ones — creates systemic risk. "
            "CISA's Critical Infrastructure Security and Resilience (CISR) program "
            "uses exactly this type of hub-failure analysis for prioritizing undersea "
            "cable protection investments."
        ),
    },
]

DEMO_SCENARIO_BY_ID: dict[str, dict] = {s["id"]: s for s in DEMO_SCENARIOS}
