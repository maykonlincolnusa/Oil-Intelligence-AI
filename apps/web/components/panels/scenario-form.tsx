"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { generateScenario } from "@/lib/api";

export function ScenarioForm() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string>("");
  const [riskDrivers, setRiskDrivers] = useState<string[]>([]);
  const [pricePressure, setPricePressure] = useState<string>("");
  const [form, setForm] = useState({
    title: "Strait of Hormuz disruption",
    event_description: "Escalating regional tensions disrupt tanker transit.",
    affected_region: "Middle East",
    affected_asset: "Shipping Lanes",
    horizon_days: 30,
    severity: "high",
  });

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    const response = await generateScenario(form);
    setResult(response.executive_summary);
    setRiskDrivers(response.risk_drivers);
    setPricePressure(response.price_pressure);
    setLoading(false);
  }

  return (
    <Card>
      <CardTitle className="mb-2">Scenario Generator</CardTitle>
      <CardDescription className="mb-4">Generate AI-supported multi-case oil market scenario analysis.</CardDescription>
      <form className="space-y-3" onSubmit={onSubmit}>
        <Input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
        <Input
          value={form.event_description}
          onChange={(e) => setForm({ ...form, event_description: e.target.value })}
        />
        <div className="grid gap-3 md:grid-cols-2">
          <Input
            value={form.affected_region}
            onChange={(e) => setForm({ ...form, affected_region: e.target.value })}
          />
          <Input
            value={form.affected_asset}
            onChange={(e) => setForm({ ...form, affected_asset: e.target.value })}
          />
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          <Input
            type="number"
            value={form.horizon_days}
            onChange={(e) => setForm({ ...form, horizon_days: Number(e.target.value) })}
          />
          <Select value={form.severity} onChange={(e) => setForm({ ...form, severity: e.target.value })}>
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
            <option value="extreme">extreme</option>
          </Select>
        </div>
        <Button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Scenario"}
        </Button>
      </form>
      {result ? <p className="mt-4 rounded-lg bg-slate-900/50 p-3 text-sm text-slate-200">{result}</p> : null}
      {pricePressure ? (
        <div className="mt-3 rounded-lg border border-slate-800 bg-slate-900/40 p-3 text-sm text-slate-300">
          <div className="mb-2 text-xs uppercase tracking-wide text-amber-300">Price pressure: {pricePressure}</div>
          <ul className="space-y-1">
            {riskDrivers.map((driver) => (
              <li key={driver}>{driver}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </Card>
  );
}
