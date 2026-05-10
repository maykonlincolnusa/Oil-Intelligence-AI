import { AppShell } from "@/components/layout/app-shell";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";

export default function SettingsPage() {
  return (
    <AppShell>
      <h1 className="text-3xl font-semibold">Settings</h1>
      <Card>
        <CardTitle>Integration Status</CardTitle>
        <CardDescription className="mt-2">
          External API keys are optional in this MVP. When absent, connectors run in deterministic mock mode.
        </CardDescription>
        <ul className="mt-4 space-y-2 text-sm text-slate-300">
          <li>Market feeds: EIA/FRED mock adapters enabled</li>
          <li>Event feeds: GDELT mock adapter enabled</li>
          <li>Satellite feeds: Sentinel/NASA/commercial placeholders enabled</li>
          <li>Daily intelligence reports: AI summary + PDF export enabled</li>
          <li>Alert framework: enterprise rule engine enabled</li>
          <li>Vector/RAG: pgvector-ready JSON fallback active</li>
          <li>Database extensibility: TimescaleDB/PostGIS migration-ready</li>
        </ul>
      </Card>
    </AppShell>
  );
}
