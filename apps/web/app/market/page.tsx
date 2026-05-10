import { AppShell } from "@/components/layout/app-shell";
import { PriceChart } from "@/components/charts/price-chart";
import { FundamentalsTable } from "@/components/panels/fundamentals-table";
import { getFundamentals, getPrices } from "@/lib/api";

export default async function MarketPage() {
  const [brent, wti, fundamentals] = await Promise.all([getPrices("BRENT"), getPrices("WTI"), getFundamentals()]);

  return (
    <AppShell>
      <h1 className="text-3xl font-semibold">Market Intelligence</h1>
      <section className="grid gap-4 xl:grid-cols-2">
        <div className="rounded-xl border border-slate-800/80 bg-panel/90 p-5">
          <h2 className="mb-4 text-lg">Brent Benchmark</h2>
          <PriceChart data={brent} color="#f2b84f" />
        </div>
        <div className="rounded-xl border border-slate-800/80 bg-panel/90 p-5">
          <h2 className="mb-4 text-lg">WTI Benchmark</h2>
          <PriceChart data={wti} color="#4ac8ff" />
        </div>
      </section>
      <FundamentalsTable items={fundamentals} />
    </AppShell>
  );
}
