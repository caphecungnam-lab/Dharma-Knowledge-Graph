"use client";

import { GraphCanvas } from "@/components/GraphCanvas";
import { NodeInspector } from "@/components/NodeInspector";
import { QueryBar } from "@/components/QueryBar";
import { useAuthGuard } from "@/lib/authGuard";

export default function Home() {
  const authorized = useAuthGuard();

  if (!authorized) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-ink text-sm text-slate-400">
        Checking access...
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col bg-ink text-slate-100">
      <header className="border-b border-slate-800 bg-slate-950/95 px-5 py-4">
        <div className="mx-auto flex max-w-7xl flex-col gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.28em] text-cyan-300">Dharma Knowledge Graph</p>
            <h1 className="mt-1 text-2xl font-semibold text-slate-50">Epistemic Knowledge Navigator</h1>
          </div>
          <QueryBar />
        </div>
      </header>

      <div className="mx-auto grid w-full max-w-7xl flex-1 gap-4 p-5 lg:grid-cols-[minmax(0,7fr)_minmax(320px,3fr)]">
        <GraphCanvas />
        <NodeInspector />
      </div>
    </main>
  );
}
