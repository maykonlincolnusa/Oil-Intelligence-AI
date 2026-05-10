"use client";

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { PricePoint } from "@/lib/types";

function formatDate(ts: string) {
  const d = new Date(ts);
  return `${d.getUTCMonth() + 1}/${d.getUTCDate()}`;
}

export function PriceChart({ data, color }: { data: PricePoint[]; color: string }) {
  const chartData = [...data]
    .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
    .map((point) => ({
      date: formatDate(point.timestamp),
      value: Number(point.value.toFixed(2)),
    }));

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <XAxis dataKey="date" tick={{ fill: "#90a4ba", fontSize: 11 }} />
          <YAxis tick={{ fill: "#90a4ba", fontSize: 11 }} domain={["dataMin - 2", "dataMax + 2"]} />
          <Tooltip
            contentStyle={{
              border: "1px solid #32475b",
              background: "#0e1722",
              color: "#d9e3ec",
            }}
          />
          <Line type="monotone" dataKey="value" stroke={color} strokeWidth={2.2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
