"use client";

import { Route } from "lucide-react";
import { useKnowledgeStore } from "@/store/useKnowledgeStore";

export function LearningPathView() {
  const path = useKnowledgeStore((state) => state.userPath);
  const queryHistory = useKnowledgeStore((state) => state.queryHistory);

  return (
    <footer className="grid min-h-[138px] grid-cols-[1fr_320px] gap-4 border-t border-line bg-ink px-5 py-4 max-[900px]:grid-cols-1">
      <section className="min-w-0">
        <div className="mb-3 flex items-center gap-2 text-xs uppercase text-slate-500">
          <Route size={16} />
          <span>Learning path</span>
        </div>
        <div className="flex min-w-0 items-center gap-2 overflow-x-auto pb-2">
          {path.map((item, index) => (
            <div key={`${item.id}-${index}`} className="flex shrink-0 items-center gap-2">
              <div
                className={`min-w-[132px] border px-3 py-2 ${
                  item.state === "current"
                    ? "border-lotus/60 bg-lotus/10 text-lotus"
                    : item.state === "visited"
                      ? "border-core/40 bg-core/10 text-core"
                      : "border-line bg-panel text-mist"
                }`}
              >
                <div className="truncate text-sm font-medium">{item.label}</div>
                <div className="mt-1 text-xs uppercase opacity-70">{item.state}</div>
              </div>
              {index < path.length - 1 ? <div className="h-px w-8 bg-line" /> : null}
            </div>
          ))}
        </div>
      </section>

      <section className="min-w-0 border-l border-line pl-4 max-[900px]:border-l-0 max-[900px]:pl-0">
        <div className="mb-3 text-xs uppercase text-slate-500">Recent portals</div>
        <div className="space-y-2">
          {(queryHistory.length ? queryHistory : ["death in Buddhism"]).slice(0, 3).map((query) => (
            <div key={query} className="truncate border border-line bg-panel px-3 py-2 text-sm text-mist">
              {query}
            </div>
          ))}
        </div>
      </section>
    </footer>
  );
}
