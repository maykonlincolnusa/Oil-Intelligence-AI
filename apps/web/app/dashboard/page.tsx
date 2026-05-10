import { AppShell } from "@/components/layout/app-shell";
import { PriceChart } from "@/components/charts/price-chart";
import { AnalystPanel } from "@/components/panels/analyst-panel";
import { EventTimeline } from "@/components/panels/event-timeline";
import { FundamentalsTable } from "@/components/panels/fundamentals-table";
import { MaritimeMapPlaceholder } from "@/components/panels/maritime-map-placeholder";
import { MetricCard } from "@/components/panels/metric-card";
import { getEvents, getFieldsSummary, getFundamentals, getPrices, getRiskSummary, getSatelliteSummary } from "@/lib/api";

export default async function DashboardPage() {
  const [brent, wti, fundamentals, risk, events, satellite, fields] = await Promise.all([
    getPrices("BRENT"),
    getPrices("WTI"),
    getFundamentals(),
    getRiskSummary(),
    getEvents(),
    getSatelliteSummary(),
    getFieldsSummary(),
  ]);

  return (
    <AppShell>
      <section className="space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">Global Oil Intelligence Dashboard</h1>
        <p className="text-muted">
          Unified view across market prices, geopolitical risk, maritime exposure, and physical signals.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Global Oil Risk Score" value={risk.global_risk_score} tone="danger" />
        <MetricCard label="Geopolitical Risk" value={risk.geopolitical_risk_score} tone="accent" />
        <MetricCard label="Maritime Risk" value={risk.maritime_risk_score} tone="accent" />
        <MetricCard
          label="Monitored Fields"
          value={fields.fields.length}
          tone="success"
          description="Active field intelligence entities"
        />
      </section>

      <section className="grid gap-4 xl:grid-cols-2">
        <div className="rounded-xl border border-slate-800/80 bg-panel/90 p-5">
          <h2 className="mb-4 text-lg font-medium">Brent Trend</h2>
          <PriceChart data={brent} color="#f2b84f" />
        </div>
        <div className="rounded-xl border border-slate-800/80 bg-panel/90 p-5">
          <h2 className="mb-4 text-lg font-medium">WTI Trend</h2>
          <PriceChart data={wti} color="#6bc5ff" />
        </div>
      </section>

      <section className="grid gap-4 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <EventTimeline items={events} />
        </div>
        <AnalystPanel drivers={risk.drivers} />
      </section>

      <section className="grid gap-4 xl:grid-cols-2">
        <FundamentalsTable items={fundamentals} />
        <div className="space-y-4">
          <MaritimeMapPlaceholder />
          <div className="rounded-xl border border-slate-800/80 bg-panel/90 p-5">
            <h3 className="mb-2 text-lg font-medium">Satellite Watch</h3>
            <p className="text-sm text-slate-300">Recent observations: {satellite.recent_observations}</p>
            <p className="text-sm text-slate-300">Active fire events: {satellite.active_fire_events}</p>
            <p className="text-sm text-slate-300">Potential spills: {satellite.potential_oil_spills}</p>
          </div>
        </div>
      </section>
    </AppShell>
  );
}
