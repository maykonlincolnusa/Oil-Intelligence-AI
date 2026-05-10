import { AppShell } from "@/components/layout/app-shell";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { getDailyReport, getDailyReportPDFUrl } from "@/lib/api";

export default async function ReportsPage() {
  const report = await getDailyReport();
  const pdfUrl = getDailyReportPDFUrl();

  return (
    <AppShell>
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-1">
          <h1 className="text-3xl font-semibold tracking-tight">Daily Intelligence Report</h1>
          <p className="text-muted">Institutional-grade AI briefing for oil market risk and opportunity.</p>
        </div>
        <a
          href={pdfUrl}
          target="_blank"
          rel="noreferrer"
          className="rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-slate-950 hover:brightness-110"
        >
          Export PDF
        </a>
      </div>

      <Card>
        <CardTitle className="mb-1">Executive Summary</CardTitle>
        <CardDescription className="mb-4">Date: {report.report_date}</CardDescription>
        <p className="text-sm leading-relaxed text-slate-200">{report.executive_summary}</p>
      </Card>

      <div className="grid gap-4 xl:grid-cols-2">
        <Card>
          <CardTitle className="mb-2">Benchmark Summary</CardTitle>
          <p className="text-sm leading-relaxed text-slate-300">{report.brent_wti_summary}</p>
        </Card>
        <Card>
          <CardTitle className="mb-2">Fundamentals Summary</CardTitle>
          <p className="text-sm leading-relaxed text-slate-300">{report.fundamentals_summary}</p>
        </Card>
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        <Card>
          <CardTitle className="mb-3">Top Price Movers</CardTitle>
          <div className="space-y-2">
            {report.top_price_movers.map((mover) => (
              <div key={mover.symbol} className="rounded-lg border border-slate-800 bg-slate-900/50 p-3 text-sm">
                <div className="font-medium text-slate-100">{mover.symbol}</div>
                <div className="text-slate-300">
                  {mover.last_price.toFixed(2)} / {mover.change_percent > 0 ? "+" : ""}
                  {mover.change_percent.toFixed(2)}%
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <CardTitle className="mb-3">Top Geopolitical Events</CardTitle>
          <div className="space-y-2">
            {report.top_geopolitical_events.map((event, idx) => (
              <div key={`${event.headline}-${idx}`} className="rounded-lg border border-slate-800 bg-slate-900/50 p-3">
                <div className="text-sm font-medium text-slate-100">{event.headline}</div>
                <div className="text-xs text-slate-400">
                  {event.risk_level} / {event.oil_impact} / conf {event.confidence_score.toFixed(2)}
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <div className="grid gap-4 xl:grid-cols-3">
        <Card>
          <CardTitle className="mb-2">Top Risk Drivers</CardTitle>
          <ul className="space-y-2 text-sm text-slate-300">
            {report.top_risk_drivers.map((item) => (
              <li key={item} className="rounded-lg border border-slate-800 bg-slate-900/50 px-3 py-2">
                {item}
              </li>
            ))}
          </ul>
        </Card>
        <Card>
          <CardTitle className="mb-2">Refinery/Storage Alerts</CardTitle>
          <ul className="space-y-2 text-sm text-slate-300">
            {report.refinery_storage_alerts.map((item) => (
              <li key={item} className="rounded-lg border border-slate-800 bg-slate-900/50 px-3 py-2">
                {item}
              </li>
            ))}
          </ul>
        </Card>
        <Card>
          <CardTitle className="mb-2">Scenario Watchlist</CardTitle>
          <ul className="space-y-2 text-sm text-slate-300">
            {report.scenario_watchlist.map((item) => (
              <li key={item} className="rounded-lg border border-slate-800 bg-slate-900/50 px-3 py-2">
                {item}
              </li>
            ))}
          </ul>
        </Card>
      </div>

      <Card>
        <CardTitle className="mb-2">AI Analyst Conclusion</CardTitle>
        <p className="text-sm leading-relaxed text-slate-300">{report.ai_analyst_conclusion}</p>
        <p className="mt-4 text-xs text-slate-500">{report.disclaimer}</p>
      </Card>
    </AppShell>
  );
}
