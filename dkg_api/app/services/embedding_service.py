from __future__ import annotations

import hashlib
import math

VECTOR_SIZE = 128


def embed_text(text: str) -> list[float]:
    vector = [0.0] * VECTOR_SIZE
    tokens = text.lower().split()

    if not tokens:
        return vector

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % VECTOR_SIZE
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return vector

    return [value / magnitude for value in vector]
