#!/usr/bin/env python3
"""Answer questions using only matched curated Evidence."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from search_curated_evidence import (
    DEFAULT_INPUT_PATH,
    positive_int,
    search_curated_evidence_file,
)

NO_EVIDENCE_MESSAGE = "Chưa có Evidence phù hợp trong curated corpus."
DEFAULT_LIMIT = 3
QUESTION_WORD = re.compile(r"[\wÀ-ỹ]+", re.UNICODE)
QUESTION_STOPWORDS = {
    "ai",
    "cai",
    "cho",
    "co",
    "có",
    "gi",
    "gì",
    "giac",
    "giác",
    "khang",
    "la",
    "là",
    "noi",
    "nói",
    "phap",
    "sư",
    "su",
    "thay",
    "thầy",
    "ve",
    "về",
}


def question_search_queries(question: str) -> list[str]:
    candidates = [question]
    words = QUESTION_WORD.findall(question.casefold())

    for index, word in enumerate(words):
        if word.isdigit() and index + 1 < len(words):
            candidates.append(f"{word} {words[index + 1]}")

    for index in range(len(words) - 1):
        first = words[index]
        second = words[index + 1]
        if first not in QUESTION_STOPWORDS or second not in QUESTION_STOPWORDS:
            candidates.append(f"{first} {second}")

    for word in words:
        if word.isdigit():
            candidates.append(word)

    unique_candidates: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in unique_candidates:
            unique_candidates.append(candidate)

    return unique_candidates


def retrieve_evidence(question: str, path: Path, limit: int) -> list[dict[str, Any]]:
    seen_ids: set[str] = set()
    matches: list[dict[str, Any]] = []

    for query in question_search_queries(question):
        for result in search_curated_evidence_file(query, path=path, limit=limit):
            evidence_id = str(result.get("id", ""))
            if evidence_id not in seen_ids:
                matches.append(result)
                seen_ids.add(evidence_id)

            if len(matches) >= limit:
                return matches

    return matches


def build_answer_text(results: list[dict[str, Any]]) -> str:
    if not results:
        return NO_EVIDENCE_MESSAGE

    return "\n\n".join(str(result.get("evidence_text", "")) for result in results)


def answer_result(result: dict[str, Any]) -> dict[str, Any]:
    timestamp = " -> ".join(
        value
        for value in [
            str(result.get("start_time", "")),
            str(result.get("end_time", "")),
        ]
        if value
    )
    return {
        "evidence_id": result.get("id", ""),
        "video_id": result.get("video_id", ""),
        "source_id": result.get("source_id", ""),
        "timestamp": timestamp,
        "source_url": result.get("source_url", ""),
        "speaker": result.get("speaker", ""),
        "review_status": result.get("review_status", ""),
        "curated_status": result.get("curated_status", ""),
        "citation": result.get("citation", ""),
        "evidence_text": result.get("evidence_text", ""),
    }


def answer_question(
    question: str,
    path: Path = DEFAULT_INPUT_PATH,
    limit: int = DEFAULT_LIMIT,
) -> dict[str, Any]:
    search_results = retrieve_evidence(question, path=path, limit=limit)
    evidence = [answer_result(result) for result in search_results]

    return {
        "question": question,
        "answer": build_answer_text(search_results),
        "evidence": evidence,
    }


def format_text_answer(answer: dict[str, Any]) -> str:
    lines = [
        f"question: {answer['question']}",
        f"answer: {answer['answer']}",
    ]

    for evidence in answer["evidence"]:
        lines.extend(
            [
                "",
                f"evidence id: {evidence['evidence_id']}",
                f"video_id: {evidence['video_id']}",
                f"source_id: {evidence['source_id']}",
                f"timestamp: {evidence['timestamp']}",
                f"source_url: {evidence['source_url']}",
                f"speaker: {evidence['speaker']}",
                f"review_status: {evidence['review_status']}",
                f"curated_status: {evidence['curated_status']}",
                f"citation: {evidence['citation']}",
            ]
        )

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Answer a question using only matched curated Evidence."
    )
    parser.add_argument("question", help="Question to answer from curated Evidence.")
    parser.add_argument(
        "--limit",
        type=positive_int,
        default=DEFAULT_LIMIT,
        help="Maximum number of Evidence matches to use.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print answer as JSON.",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to curated Evidence JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    answer = answer_question(args.question, path=args.path, limit=args.limit)

    if args.json:
        print(json.dumps(answer, indent=2, ensure_ascii=False))
    else:
        print(format_text_answer(answer))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
