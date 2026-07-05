from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem

API_INGEST_URL = "http://localhost:8000/ingest/concept"

CORE_SET = [
    {
        "id": "concept_impermanence",
        "label": "impermanence",
        "definition": "Impermanence means conditioned phenomena arise and pass away.",
        "tradition": "theravada",
        "source_id": "seed_data_core_impermanence",
        "source_type": "seed_data",
    },
    {
        "id": "concept_suffering",
        "label": "suffering",
        "definition": "Suffering names unsatisfactoriness in conditioned experience.",
        "tradition": "theravada",
        "source_id": "seed_data_core_suffering",
        "source_type": "seed_data",
    },
    {
        "id": "concept_non_self",
        "label": "non-self",
        "definition": "Non-self means no permanent independent self is found in phenomena.",
        "tradition": "theravada",
        "source_id": "seed_data_core_non_self",
        "source_type": "seed_data",
    },
    {
        "id": "concept_karma",
        "label": "karma",
        "definition": "Karma refers to intentional action and its consequences.",
        "tradition": "mixed",
        "source_id": "seed_data_core_karma",
        "source_type": "seed_data",
    },
    {
        "id": "concept_rebirth",
        "label": "rebirth",
        "definition": "Rebirth refers to continuity of conditioned existence across lives.",
        "tradition": "mixed",
        "source_id": "seed_data_core_rebirth",
        "source_type": "seed_data",
    },
    {
        "id": "concept_nirvana",
        "label": "nirvana",
        "definition": "Nirvana names liberation from greed, hatred, delusion, and suffering.",
        "tradition": "mixed",
        "source_id": "seed_data_core_nirvana",
        "source_type": "seed_data",
    },
    {
        "id": "concept_four_noble_truths",
        "label": "four noble truths",
        "definition": "The four noble truths frame suffering, origin, cessation, and path.",
        "tradition": "theravada",
        "source_id": "seed_data_core_four_noble_truths",
        "source_type": "seed_data",
    },
    {
        "id": "concept_eightfold_path",
        "label": "eightfold path",
        "definition": "The eightfold path names ethical, meditative, and wisdom factors.",
        "tradition": "theravada",
        "source_id": "seed_data_core_eightfold_path",
        "source_type": "seed_data",
    },
]


def main() -> int:
    validated = validate_seed_concepts(CORE_SET)
    if len(validated) != len(CORE_SET):
        print("Seed validation failed before ingestion.", file=sys.stderr)
        return 1

    ingested = []
    for concept in CORE_SET:
        try:
            post_json(API_INGEST_URL, concept)
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"Failed to ingest {concept['id']}: {error}", file=sys.stderr)
            return 1
        ingested.append(concept["id"])

    print(json.dumps({"status": "ok", "ingested": ingested}, indent=2))
    return 0


def validate_seed_concepts(concepts: list[dict[str, str]]) -> list[dict[str, object]]:
    context = []
    for concept in concepts:
        context.append(
            {
                "match": {
                    "node_id": concept["id"],
                    "score": 0.9,
                    "text": concept["definition"],
                    "tradition": concept["tradition"],
                    "source_id": concept["source_id"],
                    "source_type": concept["source_type"],
                },
                "related": [],
            }
        )
    evaluated = EpistemicTruthSystem().evaluate(context)
    return [node for node in evaluated if node.get("ai_usage_allowed") is True]


def post_json(url: str, payload: dict[str, str]) -> dict[str, object]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
