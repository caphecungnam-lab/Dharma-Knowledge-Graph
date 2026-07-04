from __future__ import annotations

from dkg_api.app.services.ai_reasoner import AIReasoner, INSUFFICIENT_ANSWER
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem
from dkg_api.app.services.prompt_builder import PromptBuilder


def context(
    node_id: str = "concept_dukkha",
    score: float = 0.95,
    text: str = "Dukkha means unsatisfactoriness.",
    tradition: str = "theravada",
    source_id: str = "source_sutta_001",
    source_type: str = "sutta",
    related: list[dict] | None = None,
) -> dict:
    return {
        "match": {
            "node_id": node_id,
            "score": score,
            "text": text,
            "tradition": tradition,
            "source_id": source_id,
            "source_type": source_type,
        },
        "related": related or [],
    }


def test_epistemic_truth_system_classifies_sutta_as_core_fact():
    system = EpistemicTruthSystem()

    evaluated = system.evaluate([context()])

    assert evaluated[0]["epistemic_type"] == "core_fact"
    assert evaluated[0]["conflict"] == {"type": "none", "severity": 0.0}
    assert evaluated[0]["traceability"]["sources"] == ["source_sutta_001"]
    assert evaluated[0]["ai_usage_allowed"] is True


def test_epistemic_truth_system_marks_missing_trace_unknown_and_disallowed():
    system = EpistemicTruthSystem()

    evaluated = system.evaluate([context(source_id="", source_type="")])

    assert evaluated[0]["epistemic_type"] == "unknown"
    assert evaluated[0]["confidence"] < 0.5
    assert evaluated[0]["ai_usage_allowed"] is False
    assert system.filter_ai_usable(evaluated) == []


def test_epistemic_truth_system_classifies_esoteric_context():
    system = EpistemicTruthSystem()

    evaluated = system.evaluate(
        [
            context(
                text="A tantra teaching within esoteric context.",
                tradition="vajrayana",
                source_type="commentary",
            )
        ]
    )

    assert evaluated[0]["epistemic_type"] == "esoteric_view"
    assert evaluated[0]["tradition_alignment"]["vajrayana"] == "aligned"


def test_conflict_analyzer_detects_doctrinal_conflict():
    system = EpistemicTruthSystem()

    evaluated = system.evaluate(
        [
            context(
                text="This view contradicts another doctrinal interpretation.",
                source_type="commentary",
            )
        ]
    )

    assert evaluated[0]["conflict"]["type"] == "doctrinal"
    assert evaluated[0]["conflict"]["severity"] > 0.0


def test_prompt_builder_uses_epistemic_type_for_tone():
    builder = PromptBuilder()

    prompt = builder.build(
        "What is dukkha?",
        [{"epistemic_type": "interpretive_view"}],
        0.95,
    )

    assert prompt["tone"] == "interpretive"


def test_ai_reasoner_returns_fail_safe_for_empty_context():
    reasoner = AIReasoner()

    answer = reasoner.generate("What is dukkha?", [])

    assert answer == {
        "answer": INSUFFICIENT_ANSWER,
        "confidence": 0.0,
    }


def test_ai_reasoner_uses_only_epistemically_validated_context():
    system = EpistemicTruthSystem()
    reasoner = AIReasoner()
    evaluated = system.evaluate([context()])
    validated = system.filter_ai_usable(evaluated)

    answer = reasoner.generate("What is dukkha?", validated)

    assert "Dukkha means unsatisfactoriness." in answer["answer"]
    assert answer["used_nodes"] == ["concept_dukkha"]
    assert answer["tradition_distribution"] == {
        "theravada": 100.0,
        "mahayana": 0.0,
        "vajrayana": 0.0,
    }
