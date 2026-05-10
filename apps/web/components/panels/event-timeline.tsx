import { Badge } from "@/components/ui/badge";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { EventItem } from "@/lib/types";

function toneFromRisk(level: string): "danger" | "accent" | "default" {
  if (level.toLowerCase() === "extreme" || level.toLowerCase() === "high") return "danger";
  if (level.toLowerCase() === "medium") return "accent";
  return "default";
}

export function EventTimeline({ items }: { items: EventItem[] }) {
  return (
    <Card>
      <CardTitle className="mb-2">Event Timeline</CardTitle>
      <CardDescription className="mb-5">Latest geopolitical and oil-relevant events</CardDescription>
      <div className="space-y-4">
        {items.slice(0, 6).map((event) => (
          <div key={event.id} className="rounded-lg border border-slate-800 bg-slate-900/40 p-3">
            <div className="mb-2 flex items-start justify-between gap-2">
              <h4 className="text-sm font-medium text-ink">{event.headline}</h4>
              <Badge variant={toneFromRisk(event.risk_level)}>{event.risk_level}</Badge>
            </div>
            <p className="text-sm text-muted">{event.description}</p>
            <div className="mt-2 text-xs uppercase tracking-wide text-slate-400">{event.oil_impact}</div>
          </div>
        ))}
      </div>
    </Card>
  );
}
