/** Shared UI contracts. Local synthetic prototype; money never uses JS arithmetic. */
export type Availability = "available" | "partial" | "unavailable";
export interface Metric {
  metric_id: string;
  metric_version: string;
  value: string | null;
  unit: string;
  availability: Availability;
  availability_reason: string | null;
  definition: string;
}
export interface Scope {
  start_date: string;
  end_date: string;
  source: string;
  platform: string | null;
  store: string | null;
  reporting_timezone: "America/New_York";
}
export interface MetricResponse {
  contract_version: "goodwill-v1";
  synthetic: true;
  filters_applied: Scope;
  metric_run_id: string | null;
  metrics: Metric[];
  coverage: { expected_days: string[]; complete_days: string[]; missing_or_partial_days: string[]; state: "complete" | "partial" | "unavailable" };
  freshness: { published_at: string | null; latest_import_at: string | null; is_last_good: boolean; publication_state: "published" | "stale_last_good" | "unpublished"; warning: string | null };
  reconciliation_state: "verified" | "unpublished";
  evidence: { row_count: number; gross_item_sales: string | null; refunds: string | null; missing_store_rows: number };
}
export interface EvidenceRow {
  version_id: string;
  record_key: string;
  file_id: string;
  batch_id: string;
  source_row_number: number;
  parser_version: string;
  rule_version: string;
  reporting_date: string;
  source_date: string;
  source_timestamp: string | null;
  platform: string;
  store_id: string | null;
  buyer_id: string | null;
  gross_item_sales: string;
  refunds: string;
  demo_net_sales: string;
  currency: "USD";
  synthetic: true;
  original_row: Record<string, unknown>;
}
export interface EvidenceResponse {
  contract_version: "goodwill-v1";
  synthetic: true;
  metric_run_id: string;
  filters_applied: Scope;
  offset: number;
  limit: number;
  total_rows: number;
  scope_total: string;
  rows: EvidenceRow[];
}
/** Surface HTTP errors. No financial calculations or mock fallback. */
export async function getMetrics(baseUrl: string, filters: Omit<Scope, "reporting_timezone">, signal?: AbortSignal): Promise<MetricResponse> {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) if (value !== null) query.set(key, value);
  const response = await fetch(`${baseUrl}/api/v1/metrics?${query}`, { signal });
  const body = await response.json();
  if (!response.ok) throw new Error(body.error?.detail ?? `HTTP ${response.status}`);
  if (body.contract_version !== "goodwill-v1" || body.synthetic !== true) throw new Error("Unsupported metric contract");
  return body as MetricResponse;
}
