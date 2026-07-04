from __future__ import annotations

import os
from typing import Any

from neo4j import GraphDatabase


class Neo4jClient:
    def __init__(self) -> None:
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        self.driver.close()

    def health(self) -> dict[str, object]:
        try:
            self.driver.verify_connectivity()
            return {"ok": True}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def execute_write(self, query: str, **parameters: Any) -> list[dict[str, Any]]:
        with self.driver.session() as session:
            result = session.execute_write(
                lambda tx: list(tx.run(query, **parameters).data())
            )
        return result

    def execute_read(self, query: str, **parameters: Any) -> list[dict[str, Any]]:
        with self.driver.session() as session:
            result = session.execute_read(
                lambda tx: list(tx.run(query, **parameters).data())
            )
        return result
