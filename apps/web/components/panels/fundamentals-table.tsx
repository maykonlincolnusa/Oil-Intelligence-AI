import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { FundamentalPoint } from "@/lib/types";

export function FundamentalsTable({ items }: { items: FundamentalPoint[] }) {
  return (
    <Card>
      <CardTitle className="mb-2">Petroleum Fundamentals</CardTitle>
      <CardDescription className="mb-4">Inventory, production, utilization and trade signals</CardDescription>
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="text-xs uppercase tracking-wider text-slate-400">
            <tr>
              <th className="px-2 py-2">Indicator</th>
              <th className="px-2 py-2">Region</th>
              <th className="px-2 py-2">Period</th>
              <th className="px-2 py-2">Value</th>
              <th className="px-2 py-2">Unit</th>
            </tr>
          </thead>
          <tbody>
            {items.slice(0, 10).map((item, idx) => (
              <tr key={`${item.indicator}-${idx}`} className="border-t border-slate-800">
                <td className="px-2 py-2">{item.indicator}</td>
                <td className="px-2 py-2">{item.region}</td>
                <td className="px-2 py-2">{item.period}</td>
                <td className="px-2 py-2">{item.value.toFixed(2)}</td>
                <td className="px-2 py-2">{item.unit}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
