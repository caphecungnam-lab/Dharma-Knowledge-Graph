from __future__ import annotations

import hashlib
import math

from dkg_api.app.cache.embedding_cache import embedding_cache

VECTOR_SIZE = 128


def embed_text(text: str) -> list[float]:
    cached = embedding_cache.get(text)
    if cached is not None:
        return cached

    vector = [0.0] * VECTOR_SIZE
    tokens = text.lower().split()

    if not tokens:
        embedding_cache.set(text, vector, ttl_seconds=3600)
        return vector

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % VECTOR_SIZE
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        embedding_cache.set(text, vector, ttl_seconds=3600)
        return vector

    normalized = [value / magnitude for value in vector]
    embedding_cache.set(text, normalized, ttl_seconds=3600)
    return normalized
