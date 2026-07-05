"use client";

import { FormEvent, useState } from "react";
import { Compass, Loader2, Search } from "lucide-react";
import { useKnowledgeStore } from "@/store/useKnowledgeStore";

export function QueryPortal() {
  const [query, setQuery] = useState("death in Buddhism");
  const submitQuery = useKnowledgeStore((state) => state.submitQuery);
  const loading = useKnowledgeStore((state) => state.loading);
  const centerNode = useKnowledgeStore((state) => state.currentGraph.center_node);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await submitQuery(query);
  }

  return (
    <header className="grid min-h-[86px] grid-cols-[minmax(220px,360px)_1fr_minmax(150px,220px)] items-center gap-4 border-b border-line bg-ink px-5 py-4 max-[900px]:grid-cols-1 max-[900px]:gap-3">
      <div className="flex min-w-0 items-center gap-3">
        <div className="grid h-10 w-10 shrink-0 place-items-center border border-lotus/40 bg-lotus/10 text-lotus shadow-glow">
          <Compass size={21} />
        </div>
        <div className="min-w-0">
          <h1 className="truncate text-lg font-semibold tracking-normal text-white">
            Dharma Knowledge Graph
          </h1>
          <p className="truncate text-sm text-mist">Epistemic map mode</p>
        </div>
      </div>

      <form onSubmit={onSubmit} className="flex min-w-0 items-center gap-2">
        <div className="flex h-12 min-w-0 flex-1 items-center gap-3 border border-line bg-panel px-4">
          <Search size={18} className="shrink-0 text-mist" />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            className="h-full min-w-0 flex-1 bg-transparent text-base text-white outline-none placeholder:text-slate-500"
            placeholder="Enter a concept or relation"
          />
        </div>
        <button
          type="submit"
          className="grid h-12 w-12 shrink-0 place-items-center border border-core/40 bg-core/15 text-core transition hover:bg-core/25 disabled:cursor-wait disabled:opacity-60"
          aria-label="Enter knowledge space"
          disabled={loading}
        >
          {loading ? <Loader2 size={18} className="animate-spin" /> : <Compass size={18} />}
        </button>
      </form>

      <div className="min-w-0 justify-self-end text-right max-[900px]:justify-self-start max-[900px]:text-left">
        <div className="text-xs uppercase text-slate-500">Center</div>
        <div className="truncate font-mono text-sm text-lotus">{centerNode ?? "map"}</div>
      </div>
    </header>
  );
}
