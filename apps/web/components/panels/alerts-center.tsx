"use client";

import { useState } from "react";

import { evaluateAlerts, getAlertEvents } from "@/lib/api";
import { AlertEvent, AlertRule } from "@/lib/types";

import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";

export function AlertsCenter({
  initialRules,
  initialEvents,
}: {
  initialRules: AlertRule[];
  initialEvents: AlertEvent[];
}) {
  const [events, setEvents] = useState<AlertEvent[]>(initialEvents);
  const [running, setRunning] = useState(false);
  const [lastRunSummary, setLastRunSummary] = useState<string>("");

  async function runEvaluation() {
    setRunning(true);
    const result = await evaluateAlerts();
    const latestEvents = await getAlertEvents();
    setEvents(latestEvents);
    setLastRunSummary(
      `Evaluated at ${new Date(result.evaluated_at).toLocaleString()} · ${result.triggered_count} triggered`
    );
    setRunning(false);
  }

  return (
    <div className="space-y-4">
      <Card>
        <div className="mb-4 flex items-center justify-between">
          <div>
            <CardTitle>Alert Rules</CardTitle>
            <CardDescription>Enterprise rule set for market and operational disruptions.</CardDescription>
          </div>
          <Button onClick={runEvaluation} disabled={running}>
            {running ? "Evaluating..." : "Run Evaluation"}
          </Button>
        </div>
        <div className="grid gap-2 md:grid-cols-2">
          {initialRules.map((rule) => (
            <div key={rule.rule_key} className="rounded-lg border border-slate-800 bg-slate-900/50 p-3">
              <div className="text-sm font-medium text-slate-100">{rule.name}</div>
              <div className="text-xs text-slate-400">{rule.description}</div>
              <div className="mt-2 text-xs text-slate-300">
                Threshold: {rule.comparator} {rule.threshold}
              </div>
            </div>
          ))}
        </div>
        {lastRunSummary ? <p className="mt-3 text-xs text-amber-300">{lastRunSummary}</p> : null}
      </Card>

      <Card>
        <CardTitle className="mb-2">Recent Alert Events</CardTitle>
        <CardDescription className="mb-4">Latest triggered conditions across risk domains.</CardDescription>
        <div className="space-y-2">
          {events.length === 0 ? (
            <p className="text-sm text-slate-400">No triggered alerts yet.</p>
          ) : (
            events.map((event, idx) => (
              <div key={`${event.rule_key}-${idx}`} className="rounded-lg border border-slate-800 bg-slate-900/50 p-3">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-medium text-slate-100">{event.rule_key}</div>
                  <div className="text-xs uppercase tracking-wide text-amber-300">{event.severity}</div>
                </div>
                <div className="mt-1 text-sm text-slate-300">{event.message}</div>
                <div className="mt-1 text-xs text-slate-500">
                  {new Date(event.triggered_at).toLocaleString()} · value:{" "}
                  {event.metric_value !== null && event.metric_value !== undefined
                    ? event.metric_value.toFixed(2)
                    : "n/a"}
                </div>
              </div>
            ))
          )}
        </div>
      </Card>
    </div>
  );
}
