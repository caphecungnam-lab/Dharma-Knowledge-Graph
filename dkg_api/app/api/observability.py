from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter

from dkg_api.app.observability.conflict_map import ConflictMap
from dkg_api.app.observability.dashboard import DAY4_REPORT, SystemHealthDashboard
from dkg_api.app.observability.drift_detector import DriftDetector
from dkg_api.app.observability.epistemic_monitor import EpistemicMonitor
from dkg_api.app.observability.timeline_tracker import TimelineTracker

router = APIRouter(prefix="/observability", tags=["observability"])


@router.get("/health")
def observability_health() -> dict[str, object]:
    return SystemHealthDashboard().build()


@router.get("/drift")
def observability_drift() -> dict[str, object]:
    report = _load_report()
    return DriftDetector().detect_from_report(report)


@router.get("/conflicts")
def observability_conflicts() -> dict[str, object]:
    report = _load_report()
    return ConflictMap().build_from_report(report)


@router.get("/timeline")
def observability_timeline() -> dict[str, object]:
    paths = sorted(Path("reports").glob("day*_corpus_report.json"))
    if DAY4_REPORT not in paths and DAY4_REPORT.exists():
        paths.append(DAY4_REPORT)
    return TimelineTracker().build_from_paths(paths)


@router.get("/dashboard")
def observability_dashboard() -> dict[str, object]:
    report = _load_report()
    dashboard = SystemHealthDashboard().build()
    dashboard["epistemic_monitor"] = EpistemicMonitor().snapshot_from_report(report)
    return dashboard


def _load_report() -> dict[str, object]:
    if not DAY4_REPORT.exists():
        return {}
    return json.loads(DAY4_REPORT.read_text(encoding="utf-8"))
