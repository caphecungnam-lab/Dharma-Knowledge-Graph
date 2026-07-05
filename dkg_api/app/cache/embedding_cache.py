from __future__ import annotations

from dkg_api.app.cache.query_cache import TTLCache


embedding_cache = TTLCache(max_size=4096, namespace="embedding")
