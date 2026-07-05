import { initialGraph } from "./seedGraph";
import type { AskResponse, KnowledgeGraph } from "./types";

const API_URL = process.env.NEXT_PUBLIC_DKG_API_URL ?? "http://localhost:8000";

export async function askPortal(query: string): Promise<AskResponse> {
  const response = await fetch(`${API_URL}/ai/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...apiKeyHeader()
    },
    body: JSON.stringify({ query })
  });

  if (!response.ok) {
    throw new Error("DKG query rejected by transport");
  }

  return response.json();
}

export async function fetchMap(conceptId: string): Promise<KnowledgeGraph> {
  const response = await fetch(`${API_URL}/map/${encodeURIComponent(conceptId)}`, {
    headers: apiKeyHeader()
  });

  if (!response.ok) {
    throw new Error("DKG map unavailable");
  }

  const payload = await response.json();
  return normalizeGraph(payload);
}

export async function enterKnowledgeSpace(query: string): Promise<KnowledgeGraph> {
  try {
    const response = await askPortal(query);
    const conceptId = response.used_nodes?.[0] ?? queryToConceptId(query);
    return await fetchMap(conceptId);
  } catch {
    return {
      ...initialGraph,
      center_node: queryToConceptId(query)
    };
  }
}

function normalizeGraph(payload: KnowledgeGraph): KnowledgeGraph {
  return {
    ...payload,
    nodes: payload.nodes ?? [],
    edges: payload.edges ?? [],
    traditions: payload.traditions ?? payload.layers
  };
}

function queryToConceptId(query: string): string {
  const normalized = query.toLowerCase();
  if (normalized.includes("death")) return "death";
  if (normalized.includes("karma")) return "karma";
  if (normalized.includes("nirvana")) return "nirvana";
  if (normalized.includes("bardo")) return "bardo";
  return "impermanence";
}

function apiKeyHeader(): Record<string, string> {
  const apiKey = process.env.NEXT_PUBLIC_DKG_API_KEY;
  return apiKey ? { "x-api-key": apiKey } : {};
}
