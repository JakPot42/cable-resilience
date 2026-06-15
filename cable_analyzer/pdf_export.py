from __future__ import annotations

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from .simulation import SimulationResult

LEVEL_COLORS_RL = {
    "CRITICAL": colors.HexColor("#dc2626"),
    "HIGH":     colors.HexColor("#ea580c"),
    "MEDIUM":   colors.HexColor("#ca8a04"),
    "LOW":      colors.HexColor("#16a34a"),
}


def generate_report(result: SimulationResult, scenario: dict, brief: str) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=LETTER,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "title", parent=styles["Title"], fontSize=16, spaceAfter=4,
        textColor=colors.HexColor("#1e3a5f"),
    )
    sub_style = ParagraphStyle(
        "sub", parent=styles["Normal"], fontSize=10, textColor=colors.grey,
        spaceAfter=12,
    )
    section_style = ParagraphStyle(
        "section", parent=styles["Heading2"], fontSize=11,
        textColor=colors.HexColor("#1e3a5f"), spaceBefore=14, spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "body", parent=styles["Normal"], fontSize=9, leading=13, spaceAfter=8,
    )
    watermark_style = ParagraphStyle(
        "watermark", parent=styles["Normal"], fontSize=28, textColor=colors.pink,
        alignment=TA_CENTER, spaceAfter=0,
    )

    story = []

    # DEMO watermark
    story.append(Paragraph("— DEMO — NOT FOR OPERATIONAL USE —", watermark_style))
    story.append(Spacer(1, 0.1 * inch))

    # Title
    story.append(Paragraph("Submarine Cable Resilience Report", title_style))
    story.append(Paragraph(
        f"Scenario: {scenario.get('name', result.scenario_id)} &nbsp;|&nbsp; "
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        sub_style,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a5f")))
    story.append(Spacer(1, 0.1 * inch))

    # Scenario description
    story.append(Paragraph("Scenario Description", section_style))
    story.append(Paragraph(scenario.get("description", ""), body_style))
    story.append(Paragraph(f"<b>Threat Actor:</b> {scenario.get('threat_actor', 'N/A')}", body_style))
    story.append(Paragraph(f"<b>NUWC Relevance:</b> {scenario.get('nuwc_relevance', 'N/A')}", body_style))

    # Impact summary table
    story.append(Paragraph("Impact Summary", section_style))
    table_data = [
        ["Metric", "Value"],
        ["Cables severed", ", ".join(result.cable_names)],
        ["Isolated landing stations", str(len(result.isolated_node_ids))],
        ["Disconnected station pairs",
         f"{result.disconnected_pairs:,} / {result.total_pairs:,} ({result.percent_pairs_disconnected}%)"],
        ["Capacity lost",
         f"{result.lost_capacity_tbps:.1f} Tbps / {result.total_capacity_tbps:.1f} Tbps ({result.percent_capacity_lost}%)"],
        ["Network fragmentation",
         f"{result.components_before} → {result.components_after} components"],
        ["Affected regions", ", ".join(result.affected_regions) or "None"],
    ]
    t = Table(table_data, colWidths=[2.5 * inch, 4 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4f8")]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)

    # Isolated stations list
    if result.isolated_node_names:
        story.append(Paragraph("Isolated Landing Stations", section_style))
        stations_text = " | ".join(result.isolated_node_names)
        story.append(Paragraph(stations_text, body_style))

    # Strategic brief
    story.append(Paragraph("Strategic Resilience Brief", section_style))
    story.append(Paragraph(brief.replace("\n", "<br/>"), body_style))

    # Honest limitations
    story.append(Paragraph("Analyst Notes & Limitations", section_style))
    limitations = [
        "This model uses 20 major cable systems from TeleGeography public data (June 2026). "
        "Actual global infrastructure includes 500+ cables.",
        "Capacity figures are approximate and reflect published design capacity, not current utilization.",
        "Repair timeline estimates are indicative; actual timelines depend on cable ship availability "
        "and permission to operate in relevant maritime zones.",
        "This tool is for educational and demonstration purposes. It does not reflect classified "
        "assessments of actual infrastructure vulnerability.",
    ]
    for lim in limitations:
        story.append(Paragraph(f"• {lim}", body_style))

    story.append(Spacer(1, 0.15 * inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
    story.append(Paragraph(
        "DIB Monitor — Submarine Cable Resilience Analyzer | DEMO USE ONLY | JakPot42",
        ParagraphStyle("footer", parent=styles["Normal"], fontSize=7,
                       textColor=colors.grey, alignment=TA_CENTER),
    ))

    doc.build(story)
    return buf.getvalue()
