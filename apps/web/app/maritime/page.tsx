import Link from "next/link";

import { AppShell } from "@/components/layout/app-shell";
import { MaritimeMapPlaceholder } from "@/components/panels/maritime-map-placeholder";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { getMaritimeChokepoints, getMaritimeRiskSummary } from "@/lib/api";

export default async function MaritimePage() {
  const [chokepoints, risk] = await Promise.all([getMaritimeChokepoints(), getMaritimeRiskSummary()]);

  return (
    <AppShell>
      <h1 className="text-3xl font-semibold">Maritime & Tanker Intelligence</h1>
      <div>
        <Link
          href="/maritime-map"
          className="inline-flex rounded-lg border border-slate-700 bg-slate-900/60 px-3 py-2 text-sm text-slate-200 hover:border-amber-400 hover:text-amber-200"
        >
          Open Interactive Maritime Map
        </Link>
      </div>
      <div className="grid gap-4 xl:grid-cols-3">
        <Card>
          <CardTitle className="mb-1">Maritime Risk Score</CardTitle>
          <CardDescription>{risk.maritime_risk_score} / 100</CardDescription>
          <div className="mt-3 space-y-2 text-sm text-slate-300">
            <p>Active anomalies: {risk.active_anomalies}</p>
            <p>High-risk routes: {risk.high_risk_routes}</p>
          </div>
        </Card>
        <Card className="xl:col-span-2">
          <CardTitle className="mb-2">Chokepoint Watchlist</CardTitle>
          <div className="grid gap-2 md:grid-cols-2">
            {chokepoints.map((cp) => (
              <div key={cp.name} className="rounded-md border border-slate-800 bg-slate-900/40 px-3 py-2 text-sm">
                <div className="font-medium">{cp.name}</div>
                <div className="text-muted">{cp.region}</div>
              </div>
            ))}
          </div>
        </Card>
      </div>
      <MaritimeMapPlaceholder />
    </AppShell>
  );
}
