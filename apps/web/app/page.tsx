import Link from "next/link";

import { Card, CardDescription, CardTitle } from "@/components/ui/card";

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col justify-center gap-8 p-6">
      <div>
        <p className="mb-2 text-xs uppercase tracking-[0.18em] text-accent">Enterprise Energy Intelligence</p>
        <h1 className="font-display text-5xl font-semibold tracking-tight text-ink">Oil Intelligence AI</h1>
        <p className="mt-4 max-w-3xl text-lg text-slate-300">
          AI-native platform for crude pricing, petroleum fundamentals, geopolitical risk, maritime
          chokepoints, satellite signals, and scenario analysis.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardTitle>Market Signals</CardTitle>
          <CardDescription>Brent/WTI curves, volatility stress, inventory dynamics.</CardDescription>
        </Card>
        <Card>
          <CardTitle>Risk Engine</CardTitle>
          <CardDescription>Composite geopolitical, maritime, supply, demand, refinery scoring.</CardDescription>
        </Card>
        <Card>
          <CardTitle>Scenario Studio</CardTitle>
          <CardDescription>Rapid base/bullish/bearish narrative generation for operations.</CardDescription>
        </Card>
      </div>

      <div>
        <Link
          href="/dashboard"
          className="inline-flex rounded-lg bg-accent px-5 py-3 font-semibold text-slate-950 hover:brightness-110"
        >
          Enter Platform
        </Link>
      </div>
    </main>
  );
}
