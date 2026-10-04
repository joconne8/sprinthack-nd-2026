/** Shared synthetic API client. Values and definitions come from the backend. */
export * from "./types";
import type { BatchResponse, EvidenceQuery, EvidenceResponse, ImportsResponse, ImportRequest, InventoryResponse, MetricQuery, MetricResponse, ResolutionResponse, Scope, StagingResponse } from "./types";

export class ApiError extends Error {
  constructor(public readonly status: number, public readonly body: unknown, detail: string) {
    super(detail);
    this.name = "ApiError";
  }
}

function queryString(filters: object): string {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value !== null && value !== undefined) query.set(key, String(value));
  }
  return query.toString();
}

async function jsonRequest<T>(baseUrl: string, path: string, signal?: AbortSignal, body?: object): Promise<T> {
  const response = await fetch(`${baseUrl.replace(/\/$/, "")}${path}`, {
    signal, method: body === undefined ? "GET" : "POST",
    ...(body === undefined ? {} : { headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }),
  });
  const result = await response.json();
  if (!response.ok) {
    // Preserve HTTP 422 batch controls/exceptions for the operations view.
    throw new ApiError(response.status, result, result?.error?.detail ?? `HTTP ${response.status}`);
  }
  if (result?.contract_version !== "goodwill-v1" || result?.synthetic !== true) {
    throw new Error("Unsupported synthetic API contract");
  }
  return result as T;
}

export function getMetrics(baseUrl: string, filters: MetricQuery | Omit<Scope, "reporting_timezone">, signal?: AbortSignal): Promise<MetricResponse> {
  return jsonRequest(baseUrl, `/api/v1/metrics?${queryString(filters)}`, signal);
}
export function getEvidence(baseUrl: string, filters: EvidenceQuery, signal?: AbortSignal): Promise<EvidenceResponse> {
  return jsonRequest(baseUrl, `/api/v1/evidence?${queryString(filters)}`, signal);
}
export function getImports(baseUrl: string, signal?: AbortSignal): Promise<ImportsResponse> {
  return jsonRequest(baseUrl, "/api/v1/imports", signal);
}
export function getImport(baseUrl: string, batchId: string, signal?: AbortSignal): Promise<BatchResponse> {
  return jsonRequest(baseUrl, `/api/v1/imports/${encodeURIComponent(batchId)}`, signal);
}
export function getImportRows(baseUrl: string, batchId: string, filters: { offset?: number; limit?: number; status?: "accepted" | "duplicate" | "corrected" | "rejected" } = {}, signal?: AbortSignal): Promise<StagingResponse> {
  return jsonRequest(baseUrl, `/api/v1/imports/${encodeURIComponent(batchId)}/rows?${queryString(filters)}`, signal);
}
export function importCsv(baseUrl: string, body: ImportRequest, signal?: AbortSignal): Promise<BatchResponse> {
  return jsonRequest(baseUrl, "/api/v1/imports", signal, body);
}
export function resolveException(baseUrl: string, exceptionId: string, resolution: string, signal?: AbortSignal): Promise<ResolutionResponse> {
  return jsonRequest(baseUrl, `/api/v1/exceptions/${encodeURIComponent(exceptionId)}/resolve`, signal, { resolution });
}
export function getInventory(baseUrl: string, filters: { start_date: string; end_date: string; snapshot_at?: string; store?: string }, signal?: AbortSignal): Promise<InventoryResponse> {
  return jsonRequest(baseUrl, `/api/v1/inventory?${queryString(filters)}`, signal);
}
