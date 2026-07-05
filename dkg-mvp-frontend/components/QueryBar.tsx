"use client";

import { FormEvent, useState } from "react";

import { fetchGraph } from "@/lib/dkgApi";
import { useDKGStore } from "@/store/useDKGStore";

export function QueryBar() {
  const query = useDKGStore((state) => state.query);
  const setQuery = useDKGStore((state) => state.setQuery);
  const setGraph = useDKGStore((state) => state.setGraph);
  const clearGraph = useDKGStore((state) => state.clearGraph);
  const setSelectedNode = useDKGStore((state) => state.setSelectedNode);
  const setStoreLoading = useDKGStore((state) => state.setLoading);
  const setError = useDKGStore((state) => state.setError);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setStoreLoading(true);
    setError(null);
    clearGraph();
    try {
      const graph = await fetchGraph(query);
      setGraph(graph);
      setSelectedNode(null);
    } catch {
      clearGraph();
      setError("Backend unreachable or epistemic validation failed");
    } finally {
      setLoading(false);
      setStoreLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex w-full items-center gap-3">
      <div className="flex min-h-12 flex-1 items-center rounded border border-slate-700 bg-slate-950/80 px-4 shadow-inner shadow-black/30">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Ask about Buddhist concepts..."
          className="h-12 w-full bg-transparent text-sm text-slate-100 outline-none placeholder:text-slate-500"
          aria-label="Knowledge space query"
        />
      </div>
      <button
        type="submit"
        className="h-12 rounded border border-cyan-500/60 bg-cyan-500 px-5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
        disabled={loading}
      >
        {loading ? "Loading" : "Map"}
      </button>
    </form>
  );
}
