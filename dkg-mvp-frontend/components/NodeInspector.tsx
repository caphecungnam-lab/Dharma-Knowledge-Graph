"use client";

import { useEffect, useMemo, useState } from "react";

import { fetchNodeDetails, type NodeDetails } from "@/lib/dkgApi";
import { useDKGStore } from "@/store/useDKGStore";

export function NodeInspector() {
  const graph = useDKGStore((state) => state.graph);
  const selectedNode = useDKGStore((state) => state.selectedNode);
  const [details, setDetails] = useState<NodeDetails | null>(null);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [detailError, setDetailError] = useState<string | null>(null);

  const connected = useMemo(() => {
    if (!graph || !selectedNode) {
      return [];
    }
    const relatedIds = graph.edges
      .filter((edge) => edge.from === selectedNode.id || edge.to === selectedNode.id)
      .map((edge) => (edge.from === selectedNode.id ? edge.to : edge.from));
    return graph.nodes.filter((node) => relatedIds.includes(node.id));
  }, [graph, selectedNode]);

  useEffect(() => {
    if (!selectedNode) {
      setDetails(null);
      setDetailError(null);
      return;
    }

    let active = true;
    setLoadingDetails(true);
    setDetailError(null);
    fetchNodeDetails(selectedNode.id)
      .then((nodeDetails) => {
        if (active) {
          setDetails(nodeDetails);
        }
      })
      .catch(() => {
        if (active) {
          setDetails(null);
          setDetailError("Backend unreachable or epistemic validation failed");
        }
      })
      .finally(() => {
        if (active) {
          setLoadingDetails(false);
        }
      });

    return () => {
      active = false;
    };
  }, [selectedNode]);

  if (!selectedNode) {
    return (
      <aside className="min-h-[520px] rounded border border-slate-800 bg-slate-900 p-5">
        <p className="text-sm text-slate-500">Select a node</p>
      </aside>
    );
  }

  return (
    <aside className="min-h-[520px] overflow-y-auto rounded border border-slate-800 bg-slate-900 p-5">
      <div className="space-y-5">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-cyan-300">Concept</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-50">
            {details?.label ?? selectedNode.label}
          </h2>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <InfoBlock
            label="Epistemic Type"
            value={(details?.epistemic_type ?? selectedNode.type).replace("_", " ")}
          />
          <InfoBlock
            label="Confidence"
            value={`${Math.round((details?.confidence ?? selectedNode.confidence) * 100)}%`}
          />
        </div>

        {loadingDetails ? (
          <p className="rounded border border-slate-800 bg-slate-950 p-3 text-sm text-slate-400">
            Retrieving node details...
          </p>
        ) : detailError ? (
          <p className="rounded border border-rose-900/70 bg-rose-950/40 p-3 text-sm text-rose-200">
            {detailError}
          </p>
        ) : details ? (
          <section>
            <h3 className="text-sm font-semibold text-slate-200">Definition</h3>
            <p className="mt-3 text-sm leading-6 text-slate-300">{details.definition}</p>
          </section>
        ) : null}

        <section>
          <h3 className="text-sm font-semibold text-slate-200">Related Metadata</h3>
          <dl className="mt-3 space-y-3 text-sm">
            <div className="flex justify-between gap-4 border-b border-slate-800 pb-2">
              <dt className="text-slate-500">Node ID</dt>
              <dd className="text-right text-slate-200">{selectedNode.id}</dd>
            </div>
            <div className="flex justify-between gap-4 border-b border-slate-800 pb-2">
              <dt className="text-slate-500">Graph Links</dt>
              <dd className="text-right text-slate-200">{connected.length}</dd>
            </div>
          </dl>
        </section>

        {details ? (
          <section>
            <h3 className="text-sm font-semibold text-slate-200">Traditions</h3>
            <dl className="mt-3 space-y-2 text-sm">
              {Object.entries(details.traditions).map(([tradition, value]) => (
                <div key={tradition} className="flex justify-between gap-4 border-b border-slate-800 pb-2">
                  <dt className="capitalize text-slate-500">{tradition}</dt>
                  <dd className="text-right text-slate-200">{String(value ?? "none")}</dd>
                </div>
              ))}
            </dl>
          </section>
        ) : null}

        {details ? (
          <section>
            <h3 className="text-sm font-semibold text-slate-200">Sources</h3>
            <div className="mt-3 space-y-2">
              {details.sources.length ? (
                details.sources.map((source) => (
                  <p key={source} className="rounded border border-slate-800 bg-slate-950 px-3 py-2 text-xs text-slate-300">
                    {source}
                  </p>
                ))
              ) : (
                <p className="text-sm text-slate-500">No source references returned</p>
              )}
            </div>
          </section>
        ) : null}

        <section>
          <h3 className="text-sm font-semibold text-slate-200">Connected Nodes</h3>
          <div className="mt-3 flex flex-wrap gap-2">
            {connected.length ? (
              connected.map((node) => (
                <span key={node.id} className="rounded border border-slate-700 px-2.5 py-1 text-xs text-slate-300">
                  {node.label}
                </span>
              ))
            ) : (
              <span className="text-sm text-slate-500">No connected nodes</span>
            )}
          </div>
        </section>
      </div>
    </aside>
  );
}

function InfoBlock({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded border border-slate-800 bg-slate-950 p-3">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 text-sm font-semibold capitalize text-slate-100">{value}</p>
    </div>
  );
}
