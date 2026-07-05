from __future__ import annotations

from contextlib import contextmanager
from time import perf_counter
from typing import Iterator

from dkg_api.app.observability.metrics import metrics


@contextmanager
def trace_step(name: str) -> Iterator[None]:
    started_at = perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (perf_counter() - started_at) * 1000
        metrics.record_step_latency(name, elapsed_ms)
