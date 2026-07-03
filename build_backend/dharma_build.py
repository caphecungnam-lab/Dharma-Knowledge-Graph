"""Minimal offline build backend for the dharma-kg src layout package."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import os
import time
import zipfile
from pathlib import Path

NAME = "dharma-kg"
NORMALIZED_NAME = "dharma_kg"
VERSION = "0.1.0"
DIST_INFO = f"{NORMALIZED_NAME}-{VERSION}.dist-info"
TAG = "py3-none-any"


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _metadata() -> str:
    return "\n".join(
        [
            "Metadata-Version: 2.1",
            f"Name: {NAME}",
            f"Version: {VERSION}",
            "Summary: Dharma Knowledge Graph utilities and local corpus tooling.",
            "Requires-Python: >=3.10",
            "",
        ]
    )


def _wheel() -> str:
    return "\n".join(
        [
            "Wheel-Version: 1.0",
            "Generator: dharma-kg-local-backend",
            "Root-Is-Purelib: true",
            f"Tag: {TAG}",
            "",
        ]
    )


def _hash_bytes(data: bytes) -> str:
    digest = hashlib.sha256(data).digest()
    encoded = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return f"sha256={encoded}"


def _record(rows: list[tuple[str, bytes]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")

    for path, data in rows:
        writer.writerow([path, _hash_bytes(data), str(len(data))])

    writer.writerow([f"{DIST_INFO}/RECORD", "", ""])
    return output.getvalue()


def _write_wheel(path: Path, files: list[tuple[str, bytes]]) -> None:
    timestamp = time.localtime(int(os.environ.get("SOURCE_DATE_EPOCH", "315532800")))
    record = _record(files).encode("utf-8")

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path, data in files:
            info = zipfile.ZipInfo(file_path, timestamp[:6])
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)

        info = zipfile.ZipInfo(f"{DIST_INFO}/RECORD", timestamp[:6])
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, record)


def _dist_info_files() -> list[tuple[str, bytes]]:
    return [
        (f"{DIST_INFO}/METADATA", _metadata().encode("utf-8")),
        (f"{DIST_INFO}/WHEEL", _wheel().encode("utf-8")),
    ]


def _wheel_name() -> str:
    return f"{NORMALIZED_NAME}-{VERSION}-{TAG}.whl"


def get_requires_for_build_wheel(config_settings=None) -> list[str]:
    return []


def get_requires_for_build_editable(config_settings=None) -> list[str]:
    return []


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None) -> str:
    dist_info_path = Path(metadata_directory) / DIST_INFO
    dist_info_path.mkdir(parents=True, exist_ok=True)
    (dist_info_path / "METADATA").write_text(_metadata(), encoding="utf-8")
    (dist_info_path / "WHEEL").write_text(_wheel(), encoding="utf-8")
    return DIST_INFO


def prepare_metadata_for_build_editable(metadata_directory, config_settings=None) -> str:
    return prepare_metadata_for_build_wheel(metadata_directory, config_settings)


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None) -> str:
    root = _project_root()
    files = _dist_info_files()

    for source_path in sorted((root / "src" / "dharma_kg").glob("*.py")):
        archive_path = f"dharma_kg/{source_path.name}"
        files.append((archive_path, source_path.read_bytes()))

    wheel_name = _wheel_name()
    _write_wheel(Path(wheel_directory) / wheel_name, files)
    return wheel_name


def build_editable(wheel_directory, config_settings=None, metadata_directory=None) -> str:
    src_path = str(_project_root() / "src")
    files = [
        (f"{NORMALIZED_NAME}.pth", f"{src_path}\n".encode("utf-8")),
        *_dist_info_files(),
    ]

    wheel_name = _wheel_name()
    _write_wheel(Path(wheel_directory) / wheel_name, files)
    return wheel_name
