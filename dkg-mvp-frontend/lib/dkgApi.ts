export type EpistemicType =
  | "core_fact"
  | "doctrinal"
  | "doctrinal_view"
  | "interpretive"
  | "interpretive_view"
  | "esoteric"
  | "esoteric_view"
  | "unknown";

export type DKGNode = {
  id: string;
  label: string;
  type: EpistemicType;
  confidence: number;
};

export type DKGEdge = {
  from: string;
  to: string;
};

export type DKGGraph = {
  nodes: DKGNode[];
  edges: DKGEdge[];
  center_node?: string;
  epistemic_layers?: Record<string, unknown>;
  confidence_map?: Record<string, number>;
};

export type NodeDetails = {
  id: string;
  label: string;
  definition: string;
  epistemic_type: EpistemicType;
  confidence: number;
  traditions: {
    theravada: unknown;
    mahayana: unknown;
    vajrayana: unknown;
  };
  sources: string[];
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? process.env.NEXT_PUBLIC_DKG_API;
const TOKEN_KEY = "dkg_access_token";

export type LoginResponse = {
  access_token: string;
  user: {
    role: "viewer" | "admin";
  };
};

export async function login(username: string, password: string): Promise<LoginResponse> {
  const response = await fetch(`${apiBase()}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  });

  if (!response.ok) {
    throw new Error("Login failed");
  }

  const payload = await response.json();
  if (!isRecord(payload) || typeof payload.access_token !== "string") {
    throw new Error("Login failed");
  }
  const user = isRecord(payload.user) ? payload.user : {};
  return {
    access_token: payload.access_token,
    user: {
      role: user.role === "admin" ? "admin" : "viewer"
    }
  };
}

export function saveToken(token: string) {
  window.localStorage.setItem(TOKEN_KEY, token);
}

export function getToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }
  return window.localStorage.getItem(TOKEN_KEY);
}

export function clearToken() {
  window.localStorage.removeItem(TOKEN_KEY);
}

export async function fetchGraph(query: string): Promise<DKGGraph> {
  const response = await fetch(`${apiBase()}/ai/ask`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ query })
  });

  if (!response.ok) {
    throw new Error("Backend unreachable or epistemic validation failed");
  }

  const payload = await response.json();
  return assertGraphResponse(payload);
}

export async function fetchNodeDetails(nodeId: string): Promise<NodeDetails> {
  const response = await fetch(`${apiBase()}/node/${encodeURIComponent(nodeId)}`, {
    headers: authHeaders()
  });

  if (!response.ok) {
    throw new Error("Backend unreachable or epistemic validation failed");
  }

  const payload = await response.json();
  return assertNodeDetails(payload);
}

function assertGraphResponse(value: unknown): DKGGraph {
  if (!isRecord(value) || !Array.isArray(value.nodes) || !Array.isArray(value.edges)) {
    throw new Error("Backend unreachable or epistemic validation failed");
  }

  return {
    nodes: value.nodes.map(assertGraphNode),
    edges: value.edges.map(assertGraphEdge),
    center_node: typeof value.center_node === "string" ? value.center_node : undefined,
    epistemic_layers: isRecord(value.epistemic_layers) ? value.epistemic_layers : undefined,
    confidence_map: isNumberMap(value.confidence_map) ? value.confidence_map : undefined
  };
}

function assertGraphNode(value: unknown): DKGNode {
  if (!isRecord(value)) {
    throw new Error("Backend unreachable or epistemic validation failed");
  }
  if (typeof value.id !== "string" || typeof value.label !== "string") {
    throw new Error("Backend unreachable or epistemic validation failed");
  }
  if (typeof value.type !== "string" || typeof value.confidence !== "number") {
    throw new Error("Backend unreachable or epistemic validation failed");
  }
  return {
    id: value.id,
    label: value.label,
    type: value.type as EpistemicType,
    confidence: value.confidence
  };
}

function assertGraphEdge(value: unknown): DKGEdge {
  if (!isRecord(value) || typeof value.from !== "string" || typeof value.to !== "string") {
    throw new Error("Backend unreachable or epistemic validation failed");
  }
  return {
    from: value.from,
    to: value.to
  };
}

function assertNodeDetails(value: unknown): NodeDetails {
  if (!isRecord(value)) {
    throw new Error("Backend unreachable or epistemic validation failed");
  }
  if (
    typeof value.id !== "string" ||
    typeof value.label !== "string" ||
    typeof value.definition !== "string" ||
    typeof value.epistemic_type !== "string" ||
    typeof value.confidence !== "number" ||
    !isRecord(value.traditions) ||
    !Array.isArray(value.sources)
  ) {
    throw new Error("Backend unreachable or epistemic validation failed");
  }

  return {
    id: value.id,
    label: value.label,
    definition: value.definition,
    epistemic_type: value.epistemic_type as EpistemicType,
    confidence: value.confidence,
    traditions: {
      theravada: value.traditions.theravada,
      mahayana: value.traditions.mahayana,
      vajrayana: value.traditions.vajrayana
    },
    sources: value.sources.map(String)
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isNumberMap(value: unknown): value is Record<string, number> {
  if (!isRecord(value)) {
    return false;
  }
  return Object.values(value).every((item) => typeof item === "number");
}

function apiBase(): string {
  if (!API_BASE) {
    throw new Error("NEXT_PUBLIC_DKG_API is not configured");
  }
  return API_BASE;
}

function authHeaders(): HeadersInit {
  const token = getToken();
  if (!token) {
    throw new Error("Missing JWT token");
  }
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`
  };
}
