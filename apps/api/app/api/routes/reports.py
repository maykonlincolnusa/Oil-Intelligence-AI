from datetime import date
from io import BytesIO

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.schemas.report import DailyReportResponse
from app.services.report_service import ReportService

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/daily", response_model=DailyReportResponse)
async def get_daily_report(
    report_date: date | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> DailyReportResponse:
    service = ReportService(session)
    report = await service.generate_daily_report(report_date=report_date)
    return DailyReportResponse(**report)


@router.post("/generate", response_model=DailyReportResponse)
async def generate_daily_report(
    report_date: date | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> DailyReportResponse:
    service = ReportService(session)
    report = await service.generate_daily_report(report_date=report_date)
    return DailyReportResponse(**report)


@router.get("/daily/pdf")
async def get_daily_report_pdf(
    report_date: date | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> StreamingResponse:
    service = ReportService(session)
    report = await service.generate_daily_report(report_date=report_date)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 48
    y = height - margin

    def add_line(text: str, size: int = 10, gap: int = 14) -> None:
        nonlocal y
        pdf.setFont("Helvetica", size)
        for chunk in _wrap_line(text, max_chars=108):
            if y < 72:
                pdf.showPage()
                y = height - margin
                pdf.setFont("Helvetica", size)
            pdf.drawString(margin, y, chunk)
            y -= gap

    pdf.setTitle("Oil Intelligence AI Daily Report")
    add_line("Oil Intelligence AI - Daily Oil Intelligence Report", size=14, gap=18)
    add_line(f"Report Date: {report['report_date']}", size=10)
    y -= 6
    add_line("Market Summary:", size=11, gap=16)
    add_line(report["market_summary"])
    y -= 4
    add_line("Top Price Movers:", size=11, gap=16)
    for mover in report["top_price_movers"]:
        add_line(
            f"- {mover['symbol']}: {mover['last_price']} ({mover['change_percent']:+.2f}%)"
        )
    y -= 4
    add_line("Top Geopolitical Events:", size=11, gap=16)
    for event in report["top_geopolitical_events"]:
        add_line(
            f"- {event['headline']} | {event['risk_level']} | {event['oil_impact']} | conf={event['confidence_score']:.2f}"
        )
    y -= 4
    add_line(
        f"Risk Scores: Global {report['risk_score']} | Maritime {report['maritime_risk_score']}",
        size=11,
        gap=16,
    )
    add_line("Refinery/Storage Alerts:", size=11, gap=16)
    for item in report["refinery_storage_alerts"]:
        add_line(f"- {item}")
    y -= 4
    add_line("Scenario Watchlist:", size=11, gap=16)
    for scenario in report["scenario_watchlist"]:
        add_line(f"- {scenario}")
    y -= 4
    add_line("Executive Summary:", size=11, gap=16)
    add_line(report["executive_summary"])
    add_line(f"Confidence: {report['confidence']:.2f}")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    filename = f"oil-intelligence-daily-report-{report['report_date']}.pdf"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)


def _wrap_line(text: str, max_chars: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines
