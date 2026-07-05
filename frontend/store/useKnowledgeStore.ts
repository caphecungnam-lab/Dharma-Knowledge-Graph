"use client";

import { create } from "zustand";
import { enterKnowledgeSpace, fetchMap } from "@/lib/api";
import { initialGraph, initialPath } from "@/lib/seedGraph";
import type { GraphNode, KnowledgeGraph, Tradition, UserPathItem } from "@/lib/types";

type KnowledgeState = {
  currentGraph: KnowledgeGraph;
  selectedNode: GraphNode | null;
  activeTraditions: Record<Tradition, boolean>;
  userPath: UserPathItem[];
  queryHistory: string[];
  hoveredNodeId: string | null;
  loading: boolean;
  setSelectedNode: (node: GraphNode | null) => void;
  setHoveredNodeId: (nodeId: string | null) => void;
  toggleTradition: (tradition: Tradition) => void;
  submitQuery: (query: string) => Promise<void>;
  expandNode: (nodeId: string) => Promise<void>;
};

export const useKnowledgeStore = create<KnowledgeState>((set, get) => ({
  currentGraph: initialGraph,
  selectedNode: initialGraph.nodes[0] ?? null,
  activeTraditions: {
    theravada: true,
    mahayana: true,
    vajrayana: true
  },
  userPath: initialPath,
  queryHistory: [],
  hoveredNodeId: null,
  loading: false,
  setSelectedNode: (node) => set({ selectedNode: node }),
  setHoveredNodeId: (nodeId) => set({ hoveredNodeId: nodeId }),
  toggleTradition: (tradition) =>
    set((state) => ({
      activeTraditions: {
        ...state.activeTraditions,
        [tradition]: !state.activeTraditions[tradition]
      }
    })),
  submitQuery: async (query) => {
    const trimmed = query.trim();
    if (!trimmed) return;

    set({ loading: true });
    const graph = await enterKnowledgeSpace(trimmed);
    const selectedNode = graph.nodes.find((node) => node.id === graph.center_node) ?? graph.nodes[0] ?? null;
    set((state) => ({
      currentGraph: graph,
      selectedNode,
      queryHistory: [trimmed, ...state.queryHistory].slice(0, 8),
      userPath: nextPath(state.userPath, selectedNode),
      loading: false
    }));
  },
  expandNode: async (nodeId) => {
    set({ loading: true });
    try {
      const graph = await fetchMap(nodeId);
      const selectedNode = graph.nodes.find((node) => node.id === nodeId) ?? graph.nodes[0] ?? null;
      set((state) => ({
        currentGraph: graph,
        selectedNode,
        userPath: nextPath(state.userPath, selectedNode),
        loading: false
      }));
    } catch {
      set({ loading: false });
    }
  }
}));

function nextPath(path: UserPathItem[], selectedNode: GraphNode | null): UserPathItem[] {
  if (!selectedNode) return path;
  const withoutCurrent = path.map((item) => ({
    ...item,
    state: item.state === "current" ? ("visited" as const) : item.state
  }));

  if (withoutCurrent.some((item) => item.id === selectedNode.id)) {
    return withoutCurrent.map((item) =>
      item.id === selectedNode.id ? { ...item, state: "current" as const } : item
    );
  }

  return [
    ...withoutCurrent,
    { id: selectedNode.id, label: selectedNode.label, state: "current" }
  ].slice(-7);
}
