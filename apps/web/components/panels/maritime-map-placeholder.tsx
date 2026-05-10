import { Card, CardDescription, CardTitle } from "@/components/ui/card";

export function MaritimeMapPlaceholder() {
  return (
    <Card className="overflow-hidden">
      <CardTitle className="mb-2">Maritime Chokepoint Map</CardTitle>
      <CardDescription className="mb-4">
        MapLibre-ready placeholder. Replace with live AIS overlays and route risk layers.
      </CardDescription>
      <div className="grid-pattern h-72 rounded-lg border border-slate-700 bg-slate-900/40 p-4">
        <div className="text-sm text-slate-300">MapLibre container placeholder</div>
      </div>
    </Card>
  );
}
