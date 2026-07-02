from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_seed_data import validate_seed_files  # noqa: E402


class ValidateSeedDataTest(unittest.TestCase):
    def write_seed(self, directory: Path, name: str, data: dict) -> Path:
        path = directory / name
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_valid_seed_file_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            seed = self.write_seed(
                directory,
                "valid.json",
                {
                    "nodes": [
                        {"id": "text_sample", "type": "Text", "name": "Sample"},
                        {"id": "person_author", "type": "Person", "name": "Author"},
                    ],
                    "relationships": [
                        {
                            "source": "text_sample",
                            "type": "AUTHORED_BY",
                            "target": "person_author",
                        }
                    ],
                },
            )

            self.assertEqual(validate_seed_files([seed]), [])

    def test_invalid_node_id_format_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            seed = self.write_seed(
                directory,
                "bad_id.json",
                {
                    "nodes": [
                        {
                            "id": "Concept Bad",
                            "type": "Concept",
                            "name": "Bad",
                        }
                    ],
                    "relationships": [],
                },
            )

            errors = validate_seed_files([seed])

            self.assertTrue(
                any("invalid id format" in error for error in errors),
                errors,
            )

    def test_duplicate_relationship_is_rejected_across_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            nodes = [
                {"id": "text_sample", "type": "Text", "name": "Sample"},
                {"id": "concept_sample", "type": "Concept", "name": "Concept"},
            ]
            relationship = {
                "source": "text_sample",
                "type": "MENTIONS",
                "target": "concept_sample",
            }
            first = self.write_seed(
                directory,
                "first.json",
                {"nodes": nodes, "relationships": [relationship]},
            )
            second = self.write_seed(
                directory,
                "second.json",
                {"nodes": [], "relationships": [relationship]},
            )

            errors = validate_seed_files([first, second])

            self.assertTrue(
                any("duplicate relationship" in error for error in errors),
                errors,
            )

    def test_relationship_type_rules_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            seed = self.write_seed(
                directory,
                "bad_relationship.json",
                {
                    "nodes": [
                        {"id": "concept_author", "type": "Concept", "name": "A"},
                        {"id": "text_target", "type": "Text", "name": "B"},
                    ],
                    "relationships": [
                        {
                            "source": "concept_author",
                            "type": "AUTHORED_BY",
                            "target": "text_target",
                        }
                    ],
                },
            )

            errors = validate_seed_files([seed])

            self.assertTrue(
                any("does not allow source type" in error for error in errors),
                errors,
            )
            self.assertTrue(
                any("does not allow target type" in error for error in errors),
                errors,
            )


if __name__ == "__main__":
    unittest.main()
