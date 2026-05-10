import { AppShell } from "@/components/layout/app-shell";
import { ScenarioForm } from "@/components/panels/scenario-form";

const templates = [
  "Strait of Hormuz disruption",
  "OPEC production cut",
  "Refinery outage",
  "US crude inventory drawdown",
  "Red Sea shipping disruption",
  "Hurricane in Gulf of Mexico",
];

export default function ScenariosPage() {
  return (
    <AppShell>
      <h1 className="text-3xl font-semibold">Scenario Engine</h1>
      <p className="text-muted">Create stress-tested case analysis for operational and trading decisions.</p>
      <div className="rounded-xl border border-slate-800/80 bg-panel/90 p-5">
        <h2 className="mb-3 text-lg">Starter Templates</h2>
        <div className="grid gap-2 md:grid-cols-3">
          {templates.map((template) => (
            <div key={template} className="rounded-md border border-slate-800 bg-slate-900/40 px-3 py-2 text-sm">
              {template}
            </div>
          ))}
        </div>
      </div>
      <ScenarioForm />
    </AppShell>
  );
}
