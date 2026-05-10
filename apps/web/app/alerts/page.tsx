import { AppShell } from "@/components/layout/app-shell";
import { AlertsCenter } from "@/components/panels/alerts-center";
import { getAlertEvents, getAlertRules } from "@/lib/api";

export default async function AlertsPage() {
  const [rules, events] = await Promise.all([getAlertRules(), getAlertEvents()]);

  return (
    <AppShell>
      <div className="space-y-1">
        <h1 className="text-3xl font-semibold tracking-tight">Alerts</h1>
        <p className="text-muted">Automated triggers for market, geopolitical, and operational stress signals.</p>
      </div>
      <AlertsCenter initialRules={rules} initialEvents={events} />
    </AppShell>
  );
}
