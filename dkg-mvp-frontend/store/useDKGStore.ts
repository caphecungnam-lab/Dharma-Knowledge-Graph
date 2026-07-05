"use client";

import { create } from "zustand";

import type { DKGGraph, DKGNode } from "@/lib/dkgApi";

type DKGState = {
  graph: DKGGraph | null;
  selectedNode: DKGNode | null;
  query: string;
  loading: boolean;
  error: string | null;
  graphVersion: number;
  setGraph: (graph: DKGGraph) => void;
  clearGraph: () => void;
  setSelectedNode: (node: DKGNode | null) => void;
  setQuery: (query: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
};

export const useDKGStore = create<DKGState>((set) => ({
  graph: null,
  selectedNode: null,
  query: "",
  loading: false,
  error: null,
  graphVersion: 0,
  setGraph: (graph) =>
    set((state) => ({
      graph,
      graphVersion: state.graphVersion + 1
    })),
  clearGraph: () =>
    set((state) => ({
      graph: null,
      selectedNode: null,
      graphVersion: state.graphVersion + 1
    })),
  setSelectedNode: (selectedNode) => set({ selectedNode }),
  setQuery: (query) => set({ query }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error })
}));
