from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

VALID_SOURCE_TYPES = {
    "youtube",
    "text",
    "markdown",
    "json",
    "web",
    "local",
}

VALID_STATUSES = {
    "registered",
    "queued",
    "processed",
    "failed",
    "skipped",
}

REQUIRED_FIELDS = {
    "id",
    "teacher",
    "title",
    "source",
    "source_type",
    "created_at",
    "status",
}

TEACHER_NAMESPACE = re.compile(r"^[a-z0-9_]+$")


def validate_teacher_namespace(teacher: str) -> list[str]:
    value = str(teacher or "")
    errors: list[str] = []

    if not value:
        errors.append("teacher is required")
        return errors

    if not TEACHER_NAMESPACE.fullmatch(value):
        errors.append(
            "teacher must contain only lowercase letters, numbers, and underscores"
        )

    return errors


def validate_source_type(source_type: str) -> list[str]:
    value = str(source_type or "")
    errors: list[str] = []

    if not value:
        errors.append("source_type is required")
        return errors

    if value not in VALID_SOURCE_TYPES:
        errors.append(f"unsupported source type: {value}")

    return errors


def is_url(value: str) -> bool:
    return value.startswith(("http://", "https://"))


def local_path_exists(source: str) -> bool:
    return Path(source).exists()


def validate_source_value(
    source: str,
    source_type: str,
    check_exists: bool = True,
) -> list[str]:
    value = str(source or "")
    kind = str(source_type or "")
    errors: list[str] = []

    if not value:
        errors.append("source is required")

    if kind not in VALID_SOURCE_TYPES:
        errors.append(f"unsupported source type: {kind}")
        return errors

    if not value:
        return errors

    lowered = value.lower()

    if kind == "youtube":
        if "youtube.com" not in lowered and "youtu.be" not in lowered:
            errors.append("invalid youtube source")
        return errors

    if kind == "web":
        if not is_url(lowered):
            errors.append("invalid web source")
        return errors

    if kind == "text":
        if not lowered.endswith(".txt"):
            errors.append("text source should end with .txt")
        if check_exists and not is_url(lowered) and not local_path_exists(value):
            errors.append("text source not found")
        return errors

    if kind == "markdown":
        if not lowered.endswith(".md"):
            errors.append("markdown source should end with .md")
        if check_exists and not is_url(lowered) and not local_path_exists(value):
            errors.append("markdown source not found")
        return errors

    if kind == "json":
        if not lowered.endswith(".json"):
            errors.append("json source should end with .json")
        if check_exists and not is_url(lowered) and not local_path_exists(value):
            errors.append("json source not found")
        return errors

    if kind == "local" and check_exists and not local_path_exists(value):
        errors.append("local source not found")

    return errors


def validate_manifest_payload(
    payload: dict[str, Any],
    check_exists: bool = True,
) -> list[str]:
    if not isinstance(payload, dict):
        return ["manifest payload must be a dict"]

    errors: list[str] = []

    missing = sorted(field for field in REQUIRED_FIELDS if field not in payload)
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")

    source_type = str(payload.get("source_type", ""))
    status = str(payload.get("status", ""))

    errors.extend(validate_teacher_namespace(str(payload.get("teacher", ""))))
    errors.extend(validate_source_type(source_type))
    errors.extend(
        validate_source_value(
            str(payload.get("source", "")),
            source_type,
            check_exists=check_exists,
        )
    )

    if status and status not in VALID_STATUSES:
        errors.append(f"invalid status: {status}")
    elif not status:
        errors.append("status is required")

    if not str(payload.get("id", "")):
        errors.append("id is required")

    if not str(payload.get("created_at", "")):
        errors.append("created_at is required")

    return errors


def print_errors(errors: list[str]) -> None:
    for error in errors:
        print(f"- {error}")


def cmd_validate_source(args: argparse.Namespace) -> int:
    errors: list[str] = []
    errors.extend(validate_teacher_namespace(args.teacher))
    errors.extend(validate_source_type(args.source_type))
    errors.extend(
        validate_source_value(
            args.source,
            args.source_type,
            check_exists=not args.no_check_exists,
        )
    )

    if errors:
        print("FAIL source validation")
        print_errors(errors)
        return 1

    print("PASS source validation")
    return 0


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    if not isinstance(payload, dict):
        raise ValueError("manifest must contain a JSON object")

    return payload


def cmd_validate_manifest(args: argparse.Namespace) -> int:
    try:
        payload = load_manifest(args.path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print("FAIL manifest validation")
        print(f"- {error}")
        return 1

    errors = validate_manifest_payload(
        payload,
        check_exists=not args.no_check_exists,
    )

    if errors:
        print("FAIL manifest validation")
        print_errors(errors)
        return 1

    print("PASS manifest validation")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate source intake inputs for Dharma Knowledge Graph."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    source_parser = subparsers.add_parser(
        "validate-source",
        help="Validate a source value before intake.",
    )
    source_parser.add_argument("--source", required=True)
    source_parser.add_argument("--source-type", required=True)
    source_parser.add_argument("--teacher", required=True)
    source_parser.add_argument("--no-check-exists", action="store_true")
    source_parser.set_defaults(func=cmd_validate_source)

    manifest_parser = subparsers.add_parser(
        "validate-manifest",
        help="Validate a source manifest JSON file.",
    )
    manifest_parser.add_argument("--path", type=Path, required=True)
    manifest_parser.add_argument("--no-check-exists", action="store_true")
    manifest_parser.set_defaults(func=cmd_validate_manifest)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
