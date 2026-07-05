import type { ElementDefinition } from "cytoscape";

import type { DKGGraph } from "@/lib/dkgApi";

export function graphToCytoscapeElements(graph: DKGGraph): ElementDefinition[] {
  const nodes = graph.nodes.map((node) => ({
    data: {
      id: node.id,
      label: node.label,
      type: node.type,
      confidence: node.confidence
    }
  }));
  const edges = graph.edges.map((edge, index) => ({
    data: {
      id: `${edge.from}-${edge.to}-${index}`,
      source: edge.from,
      target: edge.to
    }
  }));
  return [...nodes, ...edges];
}
