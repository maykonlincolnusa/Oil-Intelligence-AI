export type PricePoint = {
  symbol: string;
  timestamp: string;
  value: number;
  open?: number | null;
  high?: number | null;
  low?: number | null;
  close?: number | null;
  source: string;
};

export type FundamentalPoint = {
  indicator: string;
  country: string;
  region: string;
  product_type: string;
  unit: string;
  period: string;
  value: number;
  source: string;
};

export type RiskSummary = {
  global_risk_score: number;
  geopolitical_risk_score: number;
  maritime_risk_score: number;
  supply_risk_score: number;
  demand_risk_score: number;
  refinery_risk_score: number;
  volatility_score: number;
  level: string;
  drivers: string[];
  recent_events: string[];
  affected_regions: string[];
  affected_assets: string[];
  confidence: number;
};

export type EventItem = {
  id: number;
  event_time: string;
  headline: string;
  description: string;
  oil_impact: string;
  sentiment: number;
  risk_level: string;
  categories: string[];
  affected_assets: string[];
  affected_regions: string[];
  confidence_score: number;
  source: string;
};

export type MaritimeRiskSummary = {
  maritime_risk_score: number;
  active_anomalies: number;
  high_risk_routes: number;
  chokepoint_alerts: string[];
  generated_at: string;
};

export type MaritimeRoute = {
  route_id: number;
  vessel_name: string;
  origin_port?: string | null;
  destination_port?: string | null;
  route_risk_score: number;
  status: string;
  coordinates: number[][];
};

export type SatelliteSummary = {
  recent_observations: number;
  active_fire_events: number;
  potential_oil_spills: number;
  monitored_storage_sites: number;
  monitored_refineries: number;
  top_alerts: string[];
};

export type FieldSummary = {
  field_name: string;
  country: string;
  basin: string;
  operator: string;
  active_wells: number;
  latest_total_oil_bpd: number;
};

export type FieldsSummaryResponse = {
  fields: FieldSummary[];
  production_samples: Array<{
    well_name: string;
    period_date: string;
    oil_bpd: number;
    gas_mmscfd?: number | null;
  }>;
};

export type DailyReport = {
  report_date: string;
  market_summary: string;
  brent_wti_summary: string;
  top_price_movers: Array<{
    symbol: string;
    last_price: number;
    change_percent: number;
  }>;
  top_geopolitical_events: Array<{
    headline: string;
    risk_level: string;
    oil_impact: string;
    confidence_score: number;
  }>;
  top_risk_drivers: string[];
  fundamentals_summary: string;
  risk_score: number;
  maritime_risk_score: number;
  refinery_storage_alerts: string[];
  scenario_watchlist: string[];
  ai_analyst_conclusion: string;
  disclaimer: string;
  executive_summary: string;
  confidence: number;
  generated_at: string;
};

export type ScenarioResponse = {
  executive_summary: string;
  base_case: string;
  bullish_case: string;
  bearish_case: string;
  operational_impact: string;
  affected_sectors: string[];
  price_pressure: string;
  risk_drivers: string[];
  monitoring_signals: string[];
  confidence: number;
  disclaimer: string;
  recommended_monitoring_signals: string[];
};

export type AlertRule = {
  rule_key: string;
  name: string;
  description: string;
  threshold: number;
  comparator: string;
  enabled: boolean;
};

export type AlertEvent = {
  rule_key: string;
  triggered_at: string;
  severity: string;
  message: string;
  metric_value?: number | null;
  threshold_value?: number | null;
  is_active: boolean;
};

export type AlertEvaluation = {
  evaluated_at: string;
  triggered_count: number;
  events: AlertEvent[];
};
