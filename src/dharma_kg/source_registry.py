from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
SOURCES_DIR = DATA_DIR / "sources"


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


@dataclass
class SourceRecord:
    path: Path
    data: dict[str, Any]

    @property
    def id(self) -> str:
        return str(self.data.get("id", ""))

    @property
    def teacher(self) -> str:
        return str(self.data.get("teacher", ""))

    @property
    def title(self) -> str:
        return str(self.data.get("title", ""))

    @property
    def source(self) -> str:
        return str(self.data.get("source", ""))

    @property
    def source_type(self) -> str:
        return str(self.data.get("source_type", ""))

    @property
    def status(self) -> str:
        return str(self.data.get("status", ""))


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    if not isinstance(payload, dict):
        raise ValueError(f"{path} does not contain a JSON object")

    return payload


def load_sources() -> list[SourceRecord]:
    if not SOURCES_DIR.exists():
        return []

    records: list[SourceRecord] = []

    for path in sorted(SOURCES_DIR.glob("*.json")):
        try:
            records.append(SourceRecord(path=path, data=load_json(path)))
        except Exception as exc:
            records.append(
                SourceRecord(
                    path=path,
                    data={
                        "id": "",
                        "teacher": "",
                        "title": "",
                        "source": "",
                        "source_type": "",
                        "created_at": "",
                        "status": "failed",
                        "_error": str(exc),
                    },
                )
            )

    return records


def save_record(record: SourceRecord) -> None:
    record.path.parent.mkdir(parents=True, exist_ok=True)
    with record.path.open("w", encoding="utf-8") as f:
        json.dump(record.data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def find_record_by_id(
    records: list[SourceRecord],
    source_id: str,
) -> SourceRecord | None:
    for record in records:
        if record.id == source_id:
            return record
    return None


def validate_record(record: SourceRecord) -> list[str]:
    errors: list[str] = []

    missing = sorted(field for field in REQUIRED_FIELDS if field not in record.data)
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")

    if record.status and record.status not in VALID_STATUSES:
        errors.append(f"invalid status: {record.status}")

    if not record.id:
        errors.append("empty id")

    if not record.source:
        errors.append("empty source")

    if not record.teacher:
        errors.append("empty teacher")

    if "_error" in record.data:
        errors.append(f"json error: {record.data['_error']}")

    return errors


def find_duplicate_sources(records: list[SourceRecord]) -> dict[str, int]:
    sources = [record.source for record in records if record.source]
    counts = Counter(sources)

    return {source: count for source, count in counts.items() if count > 1}


def print_table(records: list[SourceRecord]) -> None:
    if not records:
        print("No source manifests found.")
        return

    print("DKG Source Registry")
    print("=" * 80)
    print(f"{'STATUS':<12} {'TYPE':<10} {'TEACHER':<14} {'ID'}")
    print("-" * 80)

    for record in records:
        print(
            f"{record.status:<12} "
            f"{record.source_type:<10} "
            f"{record.teacher:<14} "
            f"{record.id}"
        )


def cmd_list(_: argparse.Namespace) -> int:
    records = load_sources()
    print_table(records)
    return 0


def cmd_validate(_: argparse.Namespace) -> int:
    records = load_sources()
    duplicate_sources = find_duplicate_sources(records)

    has_error = False

    print("DKG Source Registry Validation")
    print("=" * 80)

    if not records:
        print("No source manifests found.")
        return 0

    for record in records:
        errors = validate_record(record)

        if record.source in duplicate_sources:
            errors.append(
                f"duplicate source: {duplicate_sources[record.source]} copies"
            )

        if errors:
            has_error = True
            print(f"FAIL {record.path.relative_to(ROOT)}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {record.path.relative_to(ROOT)}")

    if has_error:
        print("\nSource registry validation failed.")
        return 1

    print("\nSource registry validation passed.")
    return 0


def cmd_queue(args: argparse.Namespace) -> int:
    records = load_sources()

    queued = [
        record
        for record in records
        if record.status in {"registered", "failed"}
        and (not args.teacher or record.teacher == args.teacher)
    ]

    if not queued:
        print("No queued sources found.")
        return 0

    print("DKG Source Queue")
    print("=" * 80)

    for record in queued:
        print(f"{record.status:<12} {record.teacher:<14} {record.id}")
        print(f"  source: {record.source}")

    return 0


def cmd_mark(args: argparse.Namespace) -> int:
    if args.status not in VALID_STATUSES:
        print(f"Invalid status: {args.status}")
        print(f"Valid statuses: {', '.join(sorted(VALID_STATUSES))}")
        return 1

    records = load_sources()
    record = find_record_by_id(records, args.id)
    if record is None:
        print(f"Source id not found: {args.id}")
        return 1

    old_status = record.status
    record.data["status"] = args.status
    save_record(record)
    print(f"Updated {record.id} status: {old_status} -> {args.status}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Source registry and queue gate for Dharma Knowledge Graph."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List source manifests.")
    list_parser.set_defaults(func=cmd_list)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate source manifests.",
    )
    validate_parser.set_defaults(func=cmd_validate)

    queue_parser = subparsers.add_parser(
        "queue",
        help="Show registered or failed sources waiting for processing.",
    )
    queue_parser.add_argument(
        "--teacher",
        default=None,
        help="Filter queue by teacher/corpus namespace.",
    )
    queue_parser.set_defaults(func=cmd_queue)

    mark_parser = subparsers.add_parser(
        "mark",
        help="Update one source manifest status.",
    )
    mark_parser.add_argument("--id", required=True, help="Source manifest id.")
    mark_parser.add_argument("--status", required=True, help="New source status.")
    mark_parser.set_defaults(func=cmd_mark)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
