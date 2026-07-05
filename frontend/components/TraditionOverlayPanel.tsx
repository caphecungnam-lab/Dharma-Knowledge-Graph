"use client";

import { Eye, EyeOff, Layers3 } from "lucide-react";
import { useKnowledgeStore } from "@/store/useKnowledgeStore";
import type { Tradition } from "@/lib/types";

const traditions: { id: Tradition; label: string; accent: string }[] = [
  { id: "theravada", label: "Theravada", accent: "bg-core" },
  { id: "mahayana", label: "Mahayana", accent: "bg-doctrinal" },
  { id: "vajrayana", label: "Vajrayana", accent: "bg-esoteric" }
];

export function TraditionOverlayPanel() {
  const activeTraditions = useKnowledgeStore((state) => state.activeTraditions);
  const toggleTradition = useKnowledgeStore((state) => state.toggleTradition);
  const graph = useKnowledgeStore((state) => state.currentGraph);

  return (
    <aside className="dkg-scroll min-h-0 overflow-y-auto bg-panel">
      <div className="space-y-5 p-4">
        <div className="flex items-center gap-2 text-xs uppercase text-slate-500">
          <Layers3 size={16} />
          <span>Traditions</span>
        </div>

        <div className="space-y-2">
          {traditions.map((tradition) => {
            const active = activeTraditions[tradition.id];
            return (
              <button
                key={tradition.id}
                type="button"
                onClick={() => toggleTradition(tradition.id)}
                className={`flex h-12 w-full items-center justify-between border px-3 text-left transition ${
                  active
                    ? "border-line bg-ink text-white"
                    : "border-line bg-transparent text-slate-500"
                }`}
              >
                <span className="flex min-w-0 items-center gap-3">
                  <span className={`h-2.5 w-2.5 shrink-0 rounded-full ${tradition.accent}`} />
                  <span className="truncate text-sm">{tradition.label}</span>
                </span>
                {active ? <Eye size={16} /> : <EyeOff size={16} />}
              </button>
            );
          })}
        </div>

        <section className="space-y-2">
          <h3 className="text-sm font-semibold text-slate-200">Layer emphasis</h3>
          <div className="space-y-2 text-sm text-mist">
            {traditions.map((tradition) => (
              <div key={tradition.id} className="border border-line bg-ink p-3">
                <div className="text-xs uppercase text-slate-500">{tradition.label}</div>
                <div className="mt-1 leading-5">
                  {graph.traditions?.[tradition.id]?.emphasis ?? graph.layers?.[tradition.id]?.emphasis ?? "No emphasis in current map"}
                </div>
              </div>
            ))}
          </div>
        </section>

        <EpistemicLegend />
      </div>
    </aside>
  );
}

function EpistemicLegend() {
  const rows = [
    ["core_fact", "bg-core"],
    ["doctrinal", "bg-doctrinal"],
    ["interpretive", "bg-interpretive"],
    ["esoteric", "bg-esoteric"],
    ["unknown", "bg-unknown"]
  ];

  return (
    <section className="space-y-2">
      <h3 className="text-sm font-semibold text-slate-200">Epistemic layer</h3>
      <div className="space-y-2">
        {rows.map(([label, color]) => (
          <div key={label} className="flex items-center gap-3 text-sm text-mist">
            <span className={`h-2.5 w-2.5 rounded-full ${color}`} />
            <span>{label.replaceAll("_", " ")}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
