import { AppShell } from "@/components/layout/app-shell";
import { EventTimeline } from "@/components/panels/event-timeline";
import { getEvents } from "@/lib/api";

export default async function EventsPage() {
  const events = await getEvents();

  return (
    <AppShell>
      <h1 className="text-3xl font-semibold">Events Intelligence</h1>
      <p className="text-muted">Geopolitical and macro events classified by likely oil market impact.</p>
      <EventTimeline items={events} />
    </AppShell>
  );
}
