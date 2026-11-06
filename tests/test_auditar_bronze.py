from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from auditar_bronze import audit_zip, sha256_file  # noqa: E402


def test_sha256_file(tmp_path: Path) -> None:
    source = tmp_path / "fonte.csv"
    content = b"id,valor\n1,teste\n"
    source.write_bytes(content)
    assert sha256_file(source) == hashlib.sha256(content).hexdigest()


def test_audit_zip_ignores_directories(tmp_path: Path) -> None:
    archive_path = tmp_path / "heatmaps.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("snapshot/", b"")
        archive.writestr("snapshot/a.png", b"abc")
        archive.writestr("snapshot/b.png", b"defg")
    result = audit_zip(archive_path, expected_files=2)
    assert result["presente"] is True
    assert result["arquivos"] == 2
    assert result["contagem_confere"] is True
    assert result["bytes_descompactados"] == 7


def test_audit_zip_reports_missing_file(tmp_path: Path) -> None:
    result = audit_zip(tmp_path / "ausente.zip", expected_files=3)
    assert result == {
        "arquivo": "ausente.zip",
        "presente": False,
        "arquivos_esperados": 3,
    }
