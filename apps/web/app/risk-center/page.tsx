import { AppShell } from "@/components/layout/app-shell";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { getMaritimeRiskSummary, getRiskSummary } from "@/lib/api";

const bars = [
  { key: "geopolitical_risk_score", label: "Geopolitical" },
  { key: "maritime_risk_score", label: "Maritime" },
  { key: "supply_risk_score", label: "Supply" },
  { key: "demand_risk_score", label: "Demand" },
  { key: "refinery_risk_score", label: "Refinery" },
  { key: "volatility_score", label: "Volatility" },
] as const;

export default async function RiskCenterPage() {
  const [risk, maritime] = await Promise.all([getRiskSummary(), getMaritimeRiskSummary()]);

  return (
    <AppShell>
      <div className="space-y-1">
        <h1 className="text-3xl font-semibold tracking-tight">Risk Center</h1>
        <p className="text-muted">Cross-domain risk scoring and pressure diagnostics for decision teams.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardTitle>Global Risk</CardTitle>
          <CardDescription className="mt-2 text-4xl font-semibold text-amber-300">
            {risk.global_risk_score}
          </CardDescription>
          <div className="mt-2 text-xs uppercase tracking-wide text-slate-400">{risk.level}</div>
        </Card>
        <Card>
          <CardTitle>Maritime Risk</CardTitle>
          <CardDescription className="mt-2 text-4xl font-semibold text-amber-300">
            {maritime.maritime_risk_score}
          </CardDescription>
        </Card>
        <Card>
          <CardTitle>Active Maritime Anomalies</CardTitle>
          <CardDescription className="mt-2 text-4xl font-semibold text-slate-100">
            {maritime.active_anomalies}
          </CardDescription>
        </Card>
      </div>

      <Card>
        <CardTitle className="mb-3">Risk Domain Decomposition</CardTitle>
        <div className="space-y-3">
          {bars.map((bar) => {
            const value = risk[bar.key];
            return (
              <div key={bar.key}>
                <div className="mb-1 flex items-center justify-between text-sm text-slate-300">
                  <span>{bar.label}</span>
                  <span>{value}</span>
                </div>
                <div className="h-2 rounded-full bg-slate-800">
                  <div
                    className="h-2 rounded-full bg-gradient-to-r from-sky-400 via-amber-400 to-red-500"
                    style={{ width: `${Math.min(100, value)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </Card>

      <Card>
        <CardTitle className="mb-2">Current Drivers</CardTitle>
        <ul className="space-y-2 text-sm text-slate-300">
          {risk.drivers.map((driver) => (
            <li key={driver} className="rounded-lg border border-slate-800 bg-slate-900/50 px-3 py-2">
              {driver}
            </li>
          ))}
        </ul>
      </Card>

      <div className="grid gap-4 xl:grid-cols-2">
        <Card>
          <CardTitle className="mb-2">Affected Regions</CardTitle>
          <div className="flex flex-wrap gap-2 text-sm text-slate-300">
            {risk.affected_regions.map((region) => (
              <span key={region} className="rounded-md border border-slate-800 bg-slate-900/50 px-3 py-1">
                {region}
              </span>
            ))}
          </div>
        </Card>
        <Card>
          <CardTitle className="mb-2">Affected Assets</CardTitle>
          <div className="flex flex-wrap gap-2 text-sm text-slate-300">
            {risk.affected_assets.map((asset) => (
              <span key={asset} className="rounded-md border border-slate-800 bg-slate-900/50 px-3 py-1">
                {asset}
              </span>
            ))}
          </div>
        </Card>
      </div>
    </AppShell>
  );
}
