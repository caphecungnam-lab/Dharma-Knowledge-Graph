import type { KnowledgeGraph } from "./types";

export const initialGraph: KnowledgeGraph = {
  map_id: "map_impermanence",
  center_node: "impermanence",
  nodes: [
    {
      id: "impermanence",
      label: "Impermanence",
      definition: "Conditioned phenomena arise and pass away.",
      epistemic_type: "core_fact",
      confidence: 0.94,
      importance_score: 1,
      tradition: "theravada",
      source_references: ["seed_data_core_impermanence"],
      position: { x: 0, y: 0 }
    },
    {
      id: "suffering",
      label: "Suffering",
      definition: "Unsatisfactoriness in conditioned experience.",
      epistemic_type: "core_fact",
      confidence: 0.9,
      importance_score: 0.88,
      tradition: "theravada",
      source_references: ["seed_data_core_suffering"],
      position: { x: 160, y: 40 }
    },
    {
      id: "karma",
      label: "Karma",
      definition: "Intentional action and its consequences.",
      epistemic_type: "doctrinal",
      confidence: 0.78,
      importance_score: 0.78,
      tradition: "mixed",
      source_references: ["seed_data_core_karma"],
      position: { x: 320, y: -40 }
    },
    {
      id: "rebirth",
      label: "Rebirth",
      definition: "Continuity of conditioned existence across lives.",
      epistemic_type: "interpretive",
      confidence: 0.68,
      importance_score: 0.72,
      tradition: "mixed",
      source_references: ["seed_data_core_rebirth"],
      position: { x: 500, y: 60 }
    },
    {
      id: "nirvana",
      label: "Nirvana",
      definition: "Liberation from greed, hatred, delusion, and suffering.",
      epistemic_type: "core_fact",
      confidence: 0.86,
      importance_score: 0.92,
      tradition: "mixed",
      source_references: ["seed_data_core_nirvana"],
      position: { x: 680, y: 0 }
    },
    {
      id: "bardo",
      label: "Bardo",
      definition: "A Vajrayana framing of transitional experience.",
      epistemic_type: "esoteric",
      confidence: 0.62,
      importance_score: 0.62,
      tradition: "vajrayana",
      source_references: ["source_tantra_001"],
      position: { x: 430, y: 190 }
    }
  ],
  edges: [
    { from: "impermanence", to: "suffering", type: "RELATED_TO", strength: 0.9 },
    { from: "suffering", to: "karma", type: "CONTEXT_FOR", strength: 0.65 },
    { from: "karma", to: "rebirth", type: "CONDITIONS", strength: 0.72 },
    { from: "rebirth", to: "nirvana", type: "CONTRASTS_WITH", strength: 0.62 },
    { from: "rebirth", to: "bardo", type: "INTERPRETIVE_DIFFERENCE", strength: 0.58 }
  ],
  traditions: {
    theravada: { emphasis: "impermanence, suffering, cessation" },
    mahayana: { emphasis: "emptiness, compassion, non-duality" },
    vajrayana: { emphasis: "bardo, transformation, esoteric framing" }
  }
};

export const initialPath = [
  { id: "impermanence", label: "Impermanence", state: "visited" as const },
  { id: "suffering", label: "Suffering", state: "current" as const },
  { id: "karma", label: "Karma", state: "recommended" as const },
  { id: "rebirth", label: "Rebirth", state: "recommended" as const },
  { id: "nirvana", label: "Nirvana", state: "recommended" as const }
];
