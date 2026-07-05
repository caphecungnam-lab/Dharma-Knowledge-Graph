"use client";

import { ConceptInspector } from "@/components/ConceptInspector";
import { KnowledgeGraphCanvas } from "@/components/KnowledgeGraphCanvas";
import { LearningPathView } from "@/components/LearningPathView";
import { QueryPortal } from "@/components/QueryPortal";
import { TraditionOverlayPanel } from "@/components/TraditionOverlayPanel";

export default function Home() {
  return (
    <main className="grid h-screen grid-rows-[auto_minmax(0,1fr)_auto] bg-ink text-slate-100">
      <QueryPortal />
      <div className="grid min-h-0 grid-rows-[minmax(360px,1fr)_minmax(260px,34vh)]">
        <KnowledgeGraphCanvas />
        <div className="grid min-h-0 grid-cols-[minmax(300px,380px)_1fr] border-b border-line max-[900px]:grid-cols-1 max-[900px]:overflow-y-auto">
          <ConceptInspector />
          <TraditionOverlayPanel />
        </div>
      </div>
      <LearningPathView />
    </main>
  );
}
