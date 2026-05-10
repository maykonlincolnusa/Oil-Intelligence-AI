import {
  AlertEvaluation,
  AlertEvent,
  AlertRule,
  DailyReport,
  EventItem,
  FieldsSummaryResponse,
  FundamentalPoint,
  MaritimeRiskSummary,
  MaritimeRoute,
  PricePoint,
  RiskSummary,
  ScenarioResponse,
  SatelliteSummary,
} from "@/lib/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function safeGet<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${path}`, {
      next: { revalidate: 30 },
    });
    if (!response.ok) return fallback;
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

export async function getPrices(symbol = "BRENT") {
  const data = await safeGet<{ items: PricePoint[] }>(`/api/market/prices?symbol=${symbol}&limit=60`, {
    items: [],
  });
  return data.items;
}

export async function getFundamentals() {
  const data = await safeGet<{ items: FundamentalPoint[] }>("/api/market/fundamentals?limit=40", {
    items: [],
  });
  return data.items;
}

export async function getEvents() {
  const data = await safeGet<{ items: EventItem[] }>("/api/events?limit=20", { items: [] });
  return data.items;
}

export async function getRiskSummary(): Promise<RiskSummary> {
  return safeGet<RiskSummary>("/api/risk/summary", {
    global_risk_score: 58,
    geopolitical_risk_score: 62,
    maritime_risk_score: 57,
    supply_risk_score: 54,
    demand_risk_score: 49,
    refinery_risk_score: 53,
    volatility_score: 41,
    level: "elevated",
    drivers: ["Fallback mode"],
    recent_events: [],
    affected_regions: ["Global"],
    affected_assets: ["global_crude_market"],
    confidence: 0.55,
  });
}

export async function getMaritimeChokepoints() {
  return safeGet<Array<{ name: string; region: string; latitude: number; longitude: number; risk_level: string }>>(
    "/api/maritime/chokepoints",
    []
  );
}

export async function getMaritimeRiskSummary(): Promise<MaritimeRiskSummary> {
  return safeGet<MaritimeRiskSummary>("/api/maritime/risk-summary", {
    maritime_risk_score: 55,
    active_anomalies: 2,
    high_risk_routes: 1,
    chokepoint_alerts: ["Fallback maritime alert"],
    generated_at: new Date().toISOString(),
  });
}

export async function getMaritimeRoutes(): Promise<MaritimeRoute[]> {
  return safeGet<MaritimeRoute[]>("/api/maritime/routes?limit=100", []);
}

export async function getSatelliteSummary(): Promise<SatelliteSummary> {
  return safeGet<SatelliteSummary>("/api/satellite/summary", {
    recent_observations: 0,
    active_fire_events: 0,
    potential_oil_spills: 0,
    monitored_storage_sites: 0,
    monitored_refineries: 0,
    top_alerts: ["Fallback satellite summary"],
  });
}

export async function getFieldsSummary(): Promise<FieldsSummaryResponse> {
  return safeGet<FieldsSummaryResponse>("/api/fields/summary", {
    fields: [],
    production_samples: [],
  });
}

export async function getDailyReport(): Promise<DailyReport> {
  return safeGet<DailyReport>("/api/reports/daily", {
    report_date: new Date().toISOString().slice(0, 10),
    market_summary: "Fallback daily report summary.",
    brent_wti_summary: "Fallback Brent/WTI summary.",
    top_price_movers: [],
    top_geopolitical_events: [],
    top_risk_drivers: ["Fallback risk driver"],
    fundamentals_summary: "Fallback fundamentals summary.",
    risk_score: 55,
    maritime_risk_score: 52,
    refinery_storage_alerts: ["Fallback refinery/storage alert"],
    scenario_watchlist: ["Fallback scenario watchlist"],
    ai_analyst_conclusion: "Fallback analyst conclusion.",
    disclaimer: "Not financial advice.",
    executive_summary: "Fallback executive summary.",
    confidence: 0.5,
    generated_at: new Date().toISOString(),
  });
}

export async function generateDailyReport(): Promise<DailyReport> {
  try {
    const response = await fetch(`${API_BASE}/api/reports/generate`, { method: "POST" });
    if (!response.ok) throw new Error("report generation failed");
    return (await response.json()) as DailyReport;
  } catch {
    return getDailyReport();
  }
}

export function getDailyReportPDFUrl() {
  return `${API_BASE}/api/reports/daily/pdf`;
}

export async function getAlertRules(): Promise<AlertRule[]> {
  return safeGet<AlertRule[]>("/api/alerts/rules", []);
}

export async function getAlertEvents(): Promise<AlertEvent[]> {
  return safeGet<AlertEvent[]>("/api/alerts/events?limit=50", []);
}

export async function evaluateAlerts(): Promise<AlertEvaluation> {
  try {
    const response = await fetch(`${API_BASE}/api/alerts/evaluate`, { method: "POST" });
    if (!response.ok) throw new Error("alert evaluation failed");
    return (await response.json()) as AlertEvaluation;
  } catch {
    return {
      evaluated_at: new Date().toISOString(),
      triggered_count: 0,
      events: [],
    };
  }
}

export async function generateScenario(payload: {
  scenario_title?: string;
  title?: string;
  event_description: string;
  affected_region: string;
  affected_asset: string;
  horizon_days: number;
  severity: string;
}): Promise<ScenarioResponse> {
  try {
    const response = await fetch(`${API_BASE}/api/scenarios/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...payload,
        scenario_title: payload.scenario_title ?? payload.title,
      }),
    });
    if (!response.ok) throw new Error("scenario generation failed");
    return (await response.json()) as ScenarioResponse;
  } catch {
    return {
      executive_summary: "Scenario engine fallback response.",
      base_case: "Base-case placeholder",
      bullish_case: "Bullish placeholder",
      bearish_case: "Bearish placeholder",
      operational_impact: "Operational placeholder",
      affected_sectors: ["Energy"],
      price_pressure: "neutral",
      risk_drivers: ["Fallback risk driver"],
      monitoring_signals: ["Brent-WTI spread"],
      confidence: 0.5,
      disclaimer: "Not financial advice.",
      recommended_monitoring_signals: ["Brent-WTI spread"],
    };
  }
}
