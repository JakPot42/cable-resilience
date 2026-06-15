from __future__ import annotations

import json

import anthropic

from .config import CLAUDE_MODEL


class AnalystError(Exception):
    pass


def generate_resilience_brief(
    scenario_name: str,
    cable_names: list[str],
    isolated_stations: list[str],
    disconnected_pairs: int,
    total_pairs: int,
    lost_capacity_tbps: float,
    total_capacity_tbps: float,
    pct_capacity_lost: float,
    affected_regions: list[str],
    api_key: str,
) -> str:
    """
    Generate a strategic resilience brief from simulation results.
    Claude analyzes impact; code has already made all numeric determinations.
    """
    payload = {
        "scenario": scenario_name,
        "cables_severed": cable_names,
        "isolated_landing_stations": isolated_stations,
        "disconnected_station_pairs": disconnected_pairs,
        "total_station_pairs": total_pairs,
        "capacity_lost_tbps": lost_capacity_tbps,
        "total_capacity_tbps": total_capacity_tbps,
        "percent_capacity_lost": pct_capacity_lost,
        "affected_regions": affected_regions,
    }

    system_prompt = (
        "You are a critical infrastructure analyst specializing in undersea cable "
        "resilience for national security purposes. Write a structured 3-paragraph "
        "strategic brief:\n"
        "1. INFRASTRUCTURE IMPACT: What was severed and what it normally carries.\n"
        "2. STRATEGIC IMPLICATIONS: Which country-pairs or regions lose connectivity "
        "and what that means for military/government/commercial communications.\n"
        "3. RESTORATION OUTLOOK: Typical repair timelines, rerouting options, and "
        "vulnerability mitigations.\n"
        "Be factual, cite the data provided, avoid speculation beyond the data. "
        "Write approximately 200-250 words. Do not use headers — write flowing paragraphs."
    )

    user_prompt = (
        f"Generate a resilience brief for this simulation result:\n"
        f"{json.dumps(payload, indent=2)}"
    )

    try:
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=400,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return msg.content[0].text.strip()
    except AnalystError:
        raise
    except Exception as exc:
        raise AnalystError(f"Claude API error: {exc}") from exc
