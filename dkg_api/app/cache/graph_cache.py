from __future__ import annotations

from dkg_api.app.cache.query_cache import TTLCache


graph_cache = TTLCache(max_size=1024, namespace="graph")
