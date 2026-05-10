import { AppShell } from "@/components/layout/app-shell";
import { MaritimeMap } from "@/components/panels/maritime-map";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { getMaritimeChokepoints, getMaritimeRiskSummary, getMaritimeRoutes } from "@/lib/api";

export default async function MaritimeMapPage() {
  const [chokepoints, routes, risk] = await Promise.all([
    getMaritimeChokepoints(),
    getMaritimeRoutes(),
    getMaritimeRiskSummary(),
  ]);

  return (
    <AppShell>
      <div className="space-y-1">
        <h1 className="text-3xl font-semibold tracking-tight">Maritime Map</h1>
        <p className="text-muted">MapLibre route intelligence for chokepoints and tanker exposure.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardTitle>Maritime Risk Score</CardTitle>
          <CardDescription className="mt-2 text-3xl font-semibold text-amber-300">
            {risk.maritime_risk_score}
          </CardDescription>
        </Card>
        <Card>
          <CardTitle>Tracked Chokepoints</CardTitle>
          <CardDescription className="mt-2 text-3xl font-semibold text-slate-100">
            {chokepoints.length}
          </CardDescription>
        </Card>
        <Card>
          <CardTitle>Tracked Routes</CardTitle>
          <CardDescription className="mt-2 text-3xl font-semibold text-slate-100">
            {routes.length}
          </CardDescription>
        </Card>
      </div>

      <MaritimeMap chokepoints={chokepoints} routes={routes} />

      <Card>
        <CardTitle className="mb-3">Route Risk Feed</CardTitle>
        <div className="grid gap-2 md:grid-cols-2">
          {routes.slice(0, 8).map((route) => (
            <div key={route.route_id} className="rounded-lg border border-slate-800 bg-slate-900/50 p-3">
              <div className="text-sm font-medium text-slate-100">Route #{route.route_id}</div>
              <div className="text-xs text-slate-400">Vessel: {route.vessel_name}</div>
              <div className="mt-1 text-xs text-amber-300">Risk score: {route.route_risk_score}</div>
            </div>
          ))}
        </div>
      </Card>
    </AppShell>
  );
}
