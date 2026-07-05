"use client";

import { useEffect, useMemo, useRef } from "react";
import type { ReactNode } from "react";
import type { Core, ElementDefinition, EventObject, Stylesheet } from "cytoscape";
import { Maximize2, Minus, Plus } from "lucide-react";
import { useKnowledgeStore } from "@/store/useKnowledgeStore";
import type { EpistemicType, GraphNode, Tradition } from "@/lib/types";

const colorByType: Record<EpistemicType, string> = {
  core_fact: "#6ee7b7",
  doctrinal: "#60a5fa",
  doctrinal_view: "#60a5fa",
  interpretive: "#c4b5fd",
  interpretive_view: "#c4b5fd",
  esoteric: "#f0abfc",
  esoteric_view: "#f0abfc",
  unknown: "#64748b"
};

export function KnowledgeGraphCanvas() {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const cyRef = useRef<Core | null>(null);
  const graph = useKnowledgeStore((state) => state.currentGraph);
  const selectedNode = useKnowledgeStore((state) => state.selectedNode);
  const activeTraditions = useKnowledgeStore((state) => state.activeTraditions);
  const hoveredNodeId = useKnowledgeStore((state) => state.hoveredNodeId);
  const setSelectedNode = useKnowledgeStore((state) => state.setSelectedNode);
  const setHoveredNodeId = useKnowledgeStore((state) => state.setHoveredNodeId);

  const nodeMap = useMemo(() => new Map(graph.nodes.map((node) => [node.id, node])), [graph.nodes]);
  const elements = useMemo(
    () => toElements(graph.nodes, graph.edges, activeTraditions),
    [activeTraditions, graph.edges, graph.nodes]
  );

  useEffect(() => {
    let mounted = true;

    async function setup() {
      if (!containerRef.current) return;
      const cytoscape = (await import("cytoscape")).default;
      if (!mounted || !containerRef.current) return;

      cyRef.current?.destroy();
      const cy = cytoscape({
        container: containerRef.current,
        elements,
        style: stylesheet(),
        layout: {
          name: "preset",
          fit: true,
          padding: 44
        },
        wheelSensitivity: 0.18,
        minZoom: 0.35,
        maxZoom: 2.4
      });

      cy.on("tap", "node", (event: EventObject) => {
        const node = nodeMap.get(event.target.id());
        if (node) setSelectedNode(node);
      });
      cy.on("mouseover", "node", (event: EventObject) => setHoveredNodeId(event.target.id()));
      cy.on("mouseout", "node", () => setHoveredNodeId(null));
      cyRef.current = cy;
    }

    setup();
    return () => {
      mounted = false;
      cyRef.current?.destroy();
      cyRef.current = null;
    };
  }, [elements, nodeMap, setHoveredNodeId, setSelectedNode]);

  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.elements().removeClass("selected connected dimmed hover");
    if (selectedNode) {
      const selected = cy.getElementById(selectedNode.id);
      selected.addClass("selected");
      selected.connectedEdges().addClass("connected");
      selected.neighborhood("node").addClass("connected");
      cy.elements().difference(selected.closedNeighborhood()).addClass("dimmed");
    }
    if (hoveredNodeId) {
      const hovered = cy.getElementById(hoveredNodeId);
      hovered.addClass("hover");
      hovered.connectedEdges().addClass("connected");
    }
  }, [hoveredNodeId, selectedNode]);

  return (
    <section className="relative min-h-0 border-b border-line bg-[radial-gradient(circle_at_50%_40%,rgba(96,165,250,0.14),transparent_38%),#070a10]">
      <div ref={containerRef} className="h-full min-h-[360px] w-full" />
      <div className="absolute right-4 top-4 flex gap-2">
        <CanvasButton label="Zoom in" onClick={() => cyRef.current?.zoom(cyRef.current.zoom() + 0.16)}>
          <Plus size={16} />
        </CanvasButton>
        <CanvasButton label="Zoom out" onClick={() => cyRef.current?.zoom(cyRef.current.zoom() - 0.16)}>
          <Minus size={16} />
        </CanvasButton>
        <CanvasButton label="Fit graph" onClick={() => cyRef.current?.fit(undefined, 42)}>
          <Maximize2 size={16} />
        </CanvasButton>
      </div>
    </section>
  );
}

function CanvasButton({
  children,
  label,
  onClick
}: {
  children: ReactNode;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      aria-label={label}
      title={label}
      onClick={onClick}
      className="grid h-9 w-9 place-items-center border border-line bg-panel/90 text-slate-200 backdrop-blur transition hover:border-core/50 hover:text-core"
    >
      {children}
    </button>
  );
}

function toElements(
  nodes: GraphNode[],
  edges: { from: string; to: string; type: string; strength: number }[],
  activeTraditions: Record<Tradition, boolean>
): ElementDefinition[] {
  const visibleNodes = new Set(nodes.map((node) => node.id));
  return [
    ...nodes.map((node, index) => {
      const tradition = normalizeTradition(node.tradition);
      const inactiveTradition = tradition ? !activeTraditions[tradition] : false;
      return {
        data: {
          id: node.id,
          label: truncate(node.label, 32),
          color: colorByType[node.epistemic_type] ?? colorByType.unknown,
          opacity: inactiveTradition ? 0.16 : Math.max(0.22, node.confidence),
          size: 30 + Math.round((node.importance_score ?? node.confidence ?? 0.5) * 34),
          border: node.epistemic_type.includes("esoteric") ? "#f0abfc" : "#edf3fb"
        },
        position: node.position ?? positionFor(index, nodes.length),
        classes: inactiveTradition ? "traditionOff" : ""
      };
    }),
    ...edges
      .filter((edge) => visibleNodes.has(edge.from) && visibleNodes.has(edge.to))
      .map((edge) => ({
        data: {
          id: `${edge.from}-${edge.to}-${edge.type}`,
          source: edge.from,
          target: edge.to,
          label: edge.type.replaceAll("_", " ").toLowerCase(),
          strength: Math.max(1, edge.strength * 4)
        }
      }))
  ];
}

function stylesheet(): Stylesheet[] {
  return [
    {
      selector: "node",
      style: {
        "background-color": "data(color)",
        "border-color": "data(border)",
        "border-width": 1.5,
        color: "#e5edf7",
        "font-size": 10,
        label: "data(label)",
        "text-margin-y": 9,
        "text-outline-color": "#05070b",
        "text-outline-width": 3,
        height: "data(size)",
        opacity: "data(opacity)",
        width: "data(size)"
      }
    },
    {
      selector: "edge",
      style: {
        "curve-style": "bezier",
        "line-color": "#334155",
        opacity: 0.52,
        "target-arrow-color": "#334155",
        "target-arrow-shape": "triangle",
        width: "data(strength)"
      }
    },
    {
      selector: ".selected",
      style: {
        "border-color": "#e3c770",
        "border-width": 4,
        opacity: 1,
        "shadow-blur": 26,
        "shadow-color": "#e3c770",
        "shadow-opacity": 0.45
      }
    },
    {
      selector: ".connected",
      style: {
        "line-color": "#6ee7b7",
        "target-arrow-color": "#6ee7b7",
        opacity: 0.95
      }
    },
    {
      selector: ".dimmed",
      style: {
        opacity: 0.18
      }
    },
    {
      selector: ".hover",
      style: {
        "border-color": "#6ee7b7",
        "border-width": 3
      }
    },
    {
      selector: ".traditionOff",
      style: {
        opacity: 0.1
      }
    }
  ];
}

function normalizeTradition(value?: string): Tradition | null {
  if (value === "theravada" || value === "mahayana" || value === "vajrayana") return value;
  return null;
}

function positionFor(index: number, total: number) {
  const angle = (Math.PI * 2 * index) / Math.max(total, 1);
  const radius = 180 + (index % 3) * 42;
  return {
    x: Math.cos(angle) * radius,
    y: Math.sin(angle) * radius
  };
}

function truncate(value: string, limit: number) {
  if (value.length <= limit) return value;
  return `${value.slice(0, limit - 1)}…`;
}
