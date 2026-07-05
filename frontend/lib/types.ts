export type EpistemicType =
  | "core_fact"
  | "doctrinal"
  | "doctrinal_view"
  | "interpretive"
  | "interpretive_view"
  | "esoteric"
  | "esoteric_view"
  | "unknown";

export type Tradition = "theravada" | "mahayana" | "vajrayana";

export type GraphNode = {
  id: string;
  label: string;
  definition?: string;
  epistemic_type: EpistemicType;
  confidence: number;
  importance_score?: number;
  tradition?: string;
  tradition_breakdown?: Partial<Record<Tradition, number | string>>;
  source_references?: string[];
  connected_nodes?: string[];
  position?: {
    x: number;
    y: number;
    z?: number;
  };
};

export type GraphEdge = {
  from: string;
  to: string;
  type: string;
  strength: number;
};

export type TraditionLayer = {
  nodes?: GraphNode[];
  edges?: GraphEdge[];
  emphasis?: string;
};

export type KnowledgeGraph = {
  map_id?: string;
  center_node?: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  traditions?: Partial<Record<Tradition, TraditionLayer>>;
  layers?: Partial<Record<Tradition, TraditionLayer>>;
};

export type AskResponse = {
  answer?: string;
  confidence?: number;
  used_nodes?: string[];
  status?: string;
  reason?: string;
};

export type UserPathItem = {
  id: string;
  label: string;
  state: "visited" | "current" | "recommended";
};
