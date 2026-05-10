import { AppShell } from "@/components/layout/app-shell";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { getFieldsSummary } from "@/lib/api";

export default async function FieldsPage() {
  const data = await getFieldsSummary();

  return (
    <AppShell>
      <h1 className="text-3xl font-semibold">Reservoir & Field Intelligence</h1>
      <div className="grid gap-4 md:grid-cols-2">
        {data.fields.map((field) => (
          <Card key={field.field_name}>
            <CardTitle>{field.field_name}</CardTitle>
            <CardDescription>
              {field.country} · {field.basin} · {field.operator}
            </CardDescription>
            <div className="mt-3 text-sm text-slate-300">
              <p>Active wells: {field.active_wells}</p>
              <p>Latest oil production: {field.latest_total_oil_bpd.toFixed(0)} bpd</p>
            </div>
          </Card>
        ))}
      </div>

      <Card>
        <CardTitle className="mb-2">Production Samples</CardTitle>
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-xs uppercase tracking-wide text-slate-400">
              <tr>
                <th className="px-2 py-2">Well</th>
                <th className="px-2 py-2">Date</th>
                <th className="px-2 py-2">Oil (bpd)</th>
                <th className="px-2 py-2">Gas (mmscfd)</th>
              </tr>
            </thead>
            <tbody>
              {data.production_samples.map((p) => (
                <tr key={`${p.well_name}-${p.period_date}`} className="border-t border-slate-800">
                  <td className="px-2 py-2">{p.well_name}</td>
                  <td className="px-2 py-2">{p.period_date}</td>
                  <td className="px-2 py-2">{p.oil_bpd.toFixed(0)}</td>
                  <td className="px-2 py-2">{p.gas_mmscfd?.toFixed(2) ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </AppShell>
  );
}
