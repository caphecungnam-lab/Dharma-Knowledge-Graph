"use client";

import { GitBranch, Network, ShieldCheck } from "lucide-react";
import type { ReactNode } from "react";
import { useKnowledgeStore } from "@/store/useKnowledgeStore";

export function ConceptInspector() {
  const node = useKnowledgeStore((state) => state.selectedNode);
  const graph = useKnowledgeStore((state) => state.currentGraph);
  const expandNode = useKnowledgeStore((state) => state.expandNode);

  if (!node) {
    return (
      <aside className="min-h-0 border-r border-line bg-panel p-4">
        <PanelTitle icon={<ShieldCheck size={16} />} title="Concept" />
      </aside>
    );
  }

  const connected = graph.edges
    .filter((edge) => edge.from === node.id || edge.to === node.id)
    .map((edge) => (edge.from === node.id ? edge.to : edge.from));

  return (
    <aside className="dkg-scroll min-h-0 overflow-y-auto border-r border-line bg-panel">
      <div className="space-y-5 p-4">
        <PanelTitle icon={<ShieldCheck size={16} />} title="Concept" />
        <div>
          <h2 className="text-xl font-semibold text-white">{node.label}</h2>
          <p className="mt-2 text-sm leading-6 text-slate-300">
            {node.definition ?? "No definition available in current map."}
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <Metric label="Confidence" value={`${Math.round(node.confidence * 100)}%`} />
          <Metric label="Layer" value={layerLabel(node.epistemic_type)} />
        </div>

        <section className="space-y-2">
          <h3 className="text-sm font-semibold text-slate-200">Tradition</h3>
          <div className="flex flex-wrap gap-2">
            <Badge label={node.tradition ?? "mixed"} />
          </div>
        </section>

        <section className="space-y-2">
          <h3 className="text-sm font-semibold text-slate-200">Sources</h3>
          <div className="space-y-2">
            {(node.source_references ?? ["trace unavailable in current payload"]).map((source) => (
              <div key={source} className="border border-line bg-ink px-3 py-2 font-mono text-xs text-mist">
                {source}
              </div>
            ))}
          </div>
        </section>

        <section className="space-y-2">
          <h3 className="flex items-center gap-2 text-sm font-semibold text-slate-200">
            <Network size={15} />
            Connected
          </h3>
          <div className="flex flex-wrap gap-2">
            {connected.slice(0, 8).map((nodeId) => (
              <Badge key={nodeId} label={nodeId} muted />
            ))}
            {connected.length === 0 ? <span className="text-sm text-mist">No visible links</span> : null}
          </div>
        </section>

        <button
          type="button"
          onClick={() => expandNode(node.id)}
          className="flex h-11 w-full items-center justify-center gap-2 border border-core/40 bg-core/10 text-sm font-medium text-core transition hover:bg-core/20"
        >
          <GitBranch size={16} />
          Expand node
        </button>
      </div>
    </aside>
  );
}

function PanelTitle({ icon, title }: { icon: ReactNode; title: string }) {
  return (
    <div className="flex items-center gap-2 text-xs uppercase text-slate-500">
      {icon}
      <span>{title}</span>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="border border-line bg-ink p-3">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="mt-1 truncate text-sm font-semibold text-white">{value}</div>
    </div>
  );
}

function Badge({ label, muted = false }: { label: string; muted?: boolean }) {
  return (
    <span className={`border px-2 py-1 text-xs ${muted ? "border-line text-mist" : "border-lotus/40 text-lotus"}`}>
      {label}
    </span>
  );
}

function layerLabel(value: string) {
  return value.replaceAll("_", " ");
}
