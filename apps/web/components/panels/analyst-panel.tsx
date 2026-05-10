import { Card, CardDescription, CardTitle } from "@/components/ui/card";

export function AnalystPanel({ drivers }: { drivers: string[] }) {
  return (
    <Card>
      <CardTitle className="mb-2">AI Analyst Panel</CardTitle>
      <CardDescription className="mb-4">Primary market risk drivers detected</CardDescription>
      <ul className="space-y-2 text-sm text-slate-300">
        {drivers.map((driver) => (
          <li key={driver} className="rounded-md border border-slate-800 bg-slate-900/40 px-3 py-2">
            {driver}
          </li>
        ))}
      </ul>
    </Card>
  );
}
