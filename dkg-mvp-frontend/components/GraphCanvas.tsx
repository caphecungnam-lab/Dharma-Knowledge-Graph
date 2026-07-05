"use client";

import cytoscape, { Core, ElementDefinition, SingularElementArgument } from "cytoscape";
import { useEffect, useMemo, useRef } from "react";

import type { DKGNode } from "@/lib/dkgApi";
import { graphToCytoscapeElements } from "@/lib/graphAdapter";
import { useDKGStore } from "@/store/useDKGStore";

const NODE_COLORS: Record<DKGNode["type"], string> = {
  core_fact: "#38bdf8",
  doctrinal: "#4ade80",
  doctrinal_view: "#4ade80",
  interpretive: "#c084fc",
  interpretive_view: "#c084fc",
  esoteric: "#f59e0b",
  esoteric_view: "#f59e0b",
  unknown: "#64748b"
};

function nodeColor(element: SingularElementArgument) {
  const type = element.data("type") as DKGNode["type"];
  return NODE_COLORS[type] ?? "#94a3b8";
}

function nodeSize(element: SingularElementArgument) {
  return 38 + Number(element.data("confidence")) * 26;
}

function nodeOpacity(element: SingularElementArgument) {
  return Math.max(0.35, Number(element.data("confidence")));
}

export function GraphCanvas() {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const cyRef = useRef<Core | null>(null);
  const graph = useDKGStore((state) => state.graph);
  const graphVersion = useDKGStore((state) => state.graphVersion);
  const selectedNode = useDKGStore((state) => state.selectedNode);
  const setSelectedNode = useDKGStore((state) => state.setSelectedNode);
  const loading = useDKGStore((state) => state.loading);
  const error = useDKGStore((state) => state.error);

  const elements = useMemo<ElementDefinition[]>(() => {
    if (!graph) {
      return [];
    }
    return graphToCytoscapeElements(graph);
  }, [graph]);

  useEffect(() => {
    if (!graph) {
      cyRef.current?.destroy();
      cyRef.current = null;
      return;
    }
    if (!containerRef.current) {
      return;
    }

    cyRef.current?.destroy();
    const cy = cytoscape({
      container: containerRef.current,
      elements,
      minZoom: 0.45,
      maxZoom: 2.5,
      style: [
        {
          selector: "node",
          style: {
            "background-color": nodeColor,
            "border-color": "#e2e8f0",
            "border-opacity": 0.28,
            "border-width": 1,
            color: "#e5e7eb",
            "font-size": 12,
            height: nodeSize,
            label: "data(label)",
            opacity: nodeOpacity,
            "overlay-opacity": 0,
            "text-outline-color": "#020617",
            "text-outline-width": 3,
            width: nodeSize
          }
        },
        {
          selector: "node:selected",
          style: {
            "border-color": "#f8fafc",
            "border-width": 3
          }
        },
        {
          selector: "edge",
          style: {
            "curve-style": "bezier",
            "line-color": "#475569",
            opacity: 0.75,
            "target-arrow-color": "#64748b",
            "target-arrow-shape": "triangle",
            width: 2
          }
        }
      ],
      layout: {
        name: "cose",
        animate: false,
        fit: true,
        padding: 48,
        nodeRepulsion: 9000,
        idealEdgeLength: 130
      }
    });

    cy.on("tap", "node", (event) => {
      const id = event.target.id();
      const node = graph.nodes.find((item) => item.id === id) ?? null;
      setSelectedNode(node);
    });

    cy.on("tap", (event) => {
      if (event.target === cy) {
        setSelectedNode(null);
      }
    });

    cyRef.current = cy;
    return () => cy.destroy();
  }, [elements, graph, graphVersion, setSelectedNode]);

  useEffect(() => {
    if (!cyRef.current) {
      return;
    }
    cyRef.current.nodes().unselect();
    if (selectedNode) {
      cyRef.current.$id(selectedNode.id).select();
    }
  }, [selectedNode]);

  return (
    <section className="relative min-h-[520px] overflow-hidden rounded border border-slate-800 bg-slate-950">
      <div className="absolute left-4 top-4 z-10 rounded border border-slate-800 bg-slate-900/90 px-3 py-2 text-xs text-slate-400">
        Knowledge Map
      </div>
      {loading ? (
        <StatusMessage text="Retrieving epistemic graph..." />
      ) : error ? (
        <StatusMessage text="Backend unreachable or epistemic validation failed" />
      ) : graph && graph.nodes.length === 0 ? (
        <StatusMessage text="No valid epistemic data found" />
      ) : !graph ? (
        <StatusMessage text="Enter a query to retrieve the epistemic graph." />
      ) : null}
      <div ref={containerRef} className="h-full min-h-[520px] w-full" />
    </section>
  );
}

function StatusMessage({ text }: { text: string }) {
  return (
    <div className="absolute inset-0 z-20 flex items-center justify-center bg-slate-950/80 px-6 text-center text-sm text-slate-300">
      {text}
    </div>
  );
}
