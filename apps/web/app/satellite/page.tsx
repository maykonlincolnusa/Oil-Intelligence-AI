import { AppShell } from "@/components/layout/app-shell";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { getSatelliteSummary } from "@/lib/api";

export default async function SatellitePage() {
  const summary = await getSatelliteSummary();

  return (
    <AppShell>
      <h1 className="text-3xl font-semibold">Satellite & Remote Sensing</h1>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <Card>
          <CardTitle>Recent Observations</CardTitle>
          <CardDescription>{summary.recent_observations}</CardDescription>
        </Card>
        <Card>
          <CardTitle>Active Fire Events</CardTitle>
          <CardDescription>{summary.active_fire_events}</CardDescription>
        </Card>
        <Card>
          <CardTitle>Potential Oil Spills</CardTitle>
          <CardDescription>{summary.potential_oil_spills}</CardDescription>
        </Card>
      </div>
      <Card>
        <CardTitle className="mb-2">Top Alerts</CardTitle>
        <ul className="space-y-2 text-sm text-slate-300">
          {summary.top_alerts.map((alert) => (
            <li key={alert} className="rounded-md border border-slate-800 bg-slate-900/40 px-3 py-2">
              {alert}
            </li>
          ))}
        </ul>
      </Card>
    </AppShell>
  );
}
