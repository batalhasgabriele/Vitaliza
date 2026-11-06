"""Auditoria reproduzível e somente leitura da camada Bronze do Vitaliza.

Produz um manifesto JSON e um inventário Markdown sem publicar amostras de
linhas, dados pessoais ou textos livres.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW_DIR = PROJECT_ROOT / "dados" / "brutos"
DEFAULT_JSON = PROJECT_ROOT / "saidas" / "auditoria_bronze" / "manifesto_bronze.json"
DEFAULT_MARKDOWN = PROJECT_ROOT / "docs" / "source_inventory.md"


@dataclass(frozen=True)
class SourceContract:
    filename: str
    expected_rows: int | None
    key_columns: tuple[str, ...]
    date_columns: tuple[str, ...]


CONTRACTS = (
    SourceContract("usuarios.csv", 64_948, ("user_id",), ("data_cadastro", "data_nascimento")),
    SourceContract("assinaturas.csv", 32_643, ("assinatura_id",), ("inicio", "data_fim")),
    SourceContract("amizades.csv", 113_480, ("seguidor_id", "seguido_id"), ("desde",)),
    SourceContract("campanha_ago26.csv", 14_120, ("user_id",), ("enviado_em",)),
    SourceContract(
        "eventos_assinatura.csv",
        275_565,
        ("user_id", "data_hora", "evento", "plano", "canal_cobranca", "detalhe"),
        ("data_hora",),
    ),
    SourceContract("pagamentos.csv", 165_548, ("pagamento_id",), ("data_hora",)),
    SourceContract("uso_mensal.csv", 591_662, ("user_id", "mes"), ("mes",)),
    SourceContract("atividades.parquet", 1_254_475, ("atividade_id",), ("inicio",)),
    SourceContract("onboarding.csv", 63_929, ("onboarding_id",), ("respondido_em",)),
    SourceContract("pesquisa_saida.csv", 643, ("resposta_id",), ("respondido_em",)),
    SourceContract("feed_posts.csv", 119_309, ("post_id",), ("data_hora",)),
    SourceContract("tickets_suporte.csv", 4_422, ("ticket_id",), ("aberto_em", "resolvido_em")),
)

HEATMAP_CONTRACTS = {
    "heatmaps_2026-07-31.zip": 12_426,
    "heatmaps_2026-09-30.zip": 13_047,
}


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def sql_literal(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").replace("'", "''")


def sql_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def source_sql(path: Path) -> str:
    literal = sql_literal(path)
    if path.suffix.lower() == ".parquet":
        return f"read_parquet('{literal}')"
    return f"read_csv_auto('{literal}', header=true, sample_size=-1)"


def scalar(connection: duckdb.DuckDBPyConnection, query: str) -> Any:
    return connection.execute(query).fetchone()[0]


def audit_table(
    connection: duckdb.DuckDBPyConnection,
    raw_dir: Path,
    contract: SourceContract,
) -> dict[str, Any]:
    path = raw_dir / contract.filename
    if not path.is_file():
        return {"arquivo": contract.filename, "presente": False, "linhas_esperadas": contract.expected_rows}

    relation = source_sql(path)
    schema_rows = connection.execute(f"DESCRIBE SELECT * FROM {relation}").fetchall()
    schema = [{"coluna": row[0], "tipo_inferido": row[1]} for row in schema_rows]
    columns = [row[0] for row in schema_rows]
    missing_keys = sorted(set(contract.key_columns) - set(columns))
    missing_dates = sorted(set(contract.date_columns) - set(columns))

    row_count = int(scalar(connection, f"SELECT count(*) FROM {relation}"))
    null_expressions = [
        f"sum(CASE WHEN {sql_identifier(column)} IS NULL THEN 1 ELSE 0 END)" for column in columns
    ]
    null_values = connection.execute(f"SELECT {', '.join(null_expressions)} FROM {relation}").fetchone()
    null_counts = {
        column: int(value or 0)
        for column, value in zip(columns, null_values, strict=True)
        if int(value or 0) > 0
    }

    duplicate_keys: int | None = None
    if not missing_keys:
        keys = ", ".join(sql_identifier(column) for column in contract.key_columns)
        duplicate_keys = int(
            scalar(
                connection,
                "SELECT coalesce(sum(n - 1), 0) FROM "
                f"(SELECT count(*) AS n FROM {relation} GROUP BY {keys} HAVING count(*) > 1)",
            )
        )

    date_ranges: dict[str, dict[str, Any]] = {}
    for column in contract.date_columns:
        if column not in columns:
            continue
        identifier = sql_identifier(column)
        parsed_date = (
            f"try_strptime({identifier}::VARCHAR, '%Y-%m')"
            if column == "mes"
            else f"try_cast({identifier} AS TIMESTAMPTZ)"
        )
        minimum, maximum, invalid = connection.execute(
            "SELECT "
            f"min({identifier}::VARCHAR), max({identifier}::VARCHAR), "
            f"sum(CASE WHEN {identifier} IS NOT NULL "
            f"AND {parsed_date} IS NULL THEN 1 ELSE 0 END) "
            f"FROM {relation}"
        ).fetchone()
        date_ranges[column] = {
            "minimo_bruto": minimum,
            "maximo_bruto": maximum,
            "valores_nao_convertiveis": int(invalid or 0),
        }

    return {
        "arquivo": contract.filename,
        "presente": True,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "linhas": row_count,
        "linhas_esperadas": contract.expected_rows,
        "contagem_confere": row_count == contract.expected_rows,
        "colunas": columns,
        "schema": schema,
        "nulos_por_coluna": null_counts,
        "chave_candidata": list(contract.key_columns),
        "colunas_chave_ausentes": missing_keys,
        "duplicidades_chave": duplicate_keys,
        "colunas_data_ausentes": missing_dates,
        "intervalos_datas": date_ranges,
    }


def audit_zip(path: Path, expected_files: int | None) -> dict[str, Any]:
    if not path.is_file():
        return {"arquivo": path.name, "presente": False, "arquivos_esperados": expected_files}
    with zipfile.ZipFile(path) as archive:
        files = [entry for entry in archive.infolist() if not entry.is_dir()]
        uncompressed_bytes = sum(entry.file_size for entry in files)
        max_file_bytes = max((entry.file_size for entry in files), default=0)
    return {
        "arquivo": path.name,
        "presente": True,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "arquivos": len(files),
        "arquivos_esperados": expected_files,
        "contagem_confere": len(files) == expected_files,
        "bytes_descompactados": uncompressed_bytes,
        "maior_arquivo_bytes": max_file_bytes,
    }


def build_manifest(raw_dir: Path) -> dict[str, Any]:
    connection = duckdb.connect(":memory:")
    try:
        tables = [audit_table(connection, raw_dir, contract) for contract in CONTRACTS]
    finally:
        connection.close()

    heatmap_dir = raw_dir / "heatmaps"
    heatmaps = [audit_zip(heatmap_dir / name, expected) for name, expected in HEATMAP_CONTRACTS.items()]
    expected_paths = {contract.filename for contract in CONTRACTS}
    expected_paths.update(f"heatmaps/{name}" for name in HEATMAP_CONTRACTS)
    actual_paths = {path.relative_to(raw_dir).as_posix() for path in raw_dir.rglob("*") if path.is_file()}

    blocking_issues: list[str] = []
    warnings: list[str] = []
    for table in tables:
        if not table["presente"]:
            blocking_issues.append(f"Fonte ausente: {table['arquivo']}")
            continue
        if not table["contagem_confere"]:
            warnings.append(
                f"Contagem divergente em {table['arquivo']}: {table['linhas']} observadas "
                f"vs. {table['linhas_esperadas']} esperadas."
            )
        if table.get("colunas_chave_ausentes"):
            blocking_issues.append(f"Chave ausente em {table['arquivo']}: {table['colunas_chave_ausentes']}")
        if table.get("duplicidades_chave"):
            warnings.append(
                f"{table['arquivo']} possui {table['duplicidades_chave']} duplicidades na chave candidata."
            )
    for heatmap in heatmaps:
        if not heatmap["presente"]:
            blocking_issues.append(f"Pacote ausente: heatmaps/{heatmap['arquivo']}")
        elif not heatmap["contagem_confere"]:
            warnings.append(
                f"Contagem divergente em {heatmap['arquivo']}: {heatmap['arquivos']} arquivos "
                f"vs. {heatmap['arquivos_esperados']} esperados."
            )

    return {
        "manifest_version": 1,
        "generated_at": datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(timespec="seconds"),
        "raw_dir": raw_dir.relative_to(PROJECT_ROOT).as_posix(),
        "policy": "somente leitura; nenhum conteúdo de linha é exportado",
        "contracts": [asdict(contract) for contract in CONTRACTS],
        "tables": tables,
        "heatmaps": heatmaps,
        "unexpected_files": sorted(actual_paths - expected_paths),
        "missing_expected_files": sorted(expected_paths - actual_paths),
        "blocking_issues": blocking_issues,
        "warnings": warnings,
        "status": "bloqueado" if blocking_issues else ("atencao" if warnings else "conforme"),
    }


def mib(value: int | None) -> str:
    return "—" if value is None else f"{value / 1024 / 1024:.2f}"


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Inventário das Fontes — Camada Bronze",
        "",
        f"- **Gerado em:** `{manifest['generated_at']}`",
        f"- **Status:** **{manifest['status'].upper()}**",
        "- **Política:** auditoria somente leitura; nenhum conteúdo de linha ou dado pessoal é publicado.",
        "- **Data de corte do case:** `30/09/2026`.",
        "",
        "## Fontes tabulares",
        "",
        "| Arquivo | Linhas observadas | Referência | Confere | Tamanho (MiB) | Duplicidades na chave candidata |",
        "|:---|---:|---:|:---:|---:|---:|",
    ]
    for table in manifest["tables"]:
        if not table["presente"]:
            lines.append(f"| `{table['arquivo']}` | ausente | {table['linhas_esperadas']} | ❌ | — | — |")
            continue
        lines.append(
            f"| `{table['arquivo']}` | {table['linhas']:,} | {table['linhas_esperadas']:,} | "
            f"{'✅' if table['contagem_confere'] else '⚠️'} | {mib(table['bytes'])} | "
            f"{table['duplicidades_chave'] if table['duplicidades_chave'] is not None else '—'} |"
        )

    lines.extend([
        "", "## Pacotes de heatmaps", "",
        "| Arquivo | Imagens observadas | Referência | Confere | Compactado (MiB) | Descompactado (MiB) |",
        "|:---|---:|---:|:---:|---:|---:|",
    ])
    for item in manifest["heatmaps"]:
        if not item["presente"]:
            lines.append(f"| `{item['arquivo']}` | ausente | {item['arquivos_esperados']} | ❌ | — | — |")
            continue
        lines.append(
            f"| `{item['arquivo']}` | {item['arquivos']:,} | {item['arquivos_esperados']:,} | "
            f"{'✅' if item['contagem_confere'] else '⚠️'} | {mib(item['bytes'])} | "
            f"{mib(item['bytes_descompactados'])} |"
        )

    lines.extend(["", "## Alertas e bloqueios", ""])
    issues = manifest["blocking_issues"] + manifest["warnings"]
    lines.extend((f"- {issue}" for issue in issues),)
    if not issues:
        lines.append("- Nenhum alerta encontrado no contrato estrutural.")

    lines.extend(["", "## Schemas e cobertura temporal", ""])
    for table in manifest["tables"]:
        if not table["presente"]:
            continue
        schema = ", ".join(
            f"`{column['coluna']}` ({column['tipo_inferido']})" for column in table["schema"]
        )
        lines.extend([f"### `{table['arquivo']}`", "", f"- **Schema inferido:** {schema}"])
        if table["nulos_por_coluna"]:
            nulls = ", ".join(
                f"`{column}`={count:,}" for column, count in table["nulos_por_coluna"].items()
            )
            lines.append(f"- **Nulos observados:** {nulls}")
        else:
            lines.append("- **Nulos observados:** nenhum.")
        for column, interval in table["intervalos_datas"].items():
            lines.append(
                f"- **{column}:** `{interval['minimo_bruto']}` a `{interval['maximo_bruto']}`; "
                f"não convertíveis: {interval['valores_nao_convertiveis']:,}."
            )
        lines.append("")

    lines.extend([
        "## Interpretação", "",
        "Este inventário valida presença, integridade de arquivo, contagens, schemas inferidos, "
        "nulos, chaves candidatas e intervalos temporais. Ele não substitui as validações "
        "semânticas e de negócio da camada Prata, que tratarão fusos, estados históricos, "
        "cobranças duplicadas e regras de elegibilidade.", "",
    ])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MARKDOWN)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw_dir = args.raw_dir.resolve()
    if not raw_dir.is_dir():
        print(f"Camada Bronze não encontrada: {raw_dir}", file=sys.stderr)
        return 2
    manifest = build_manifest(raw_dir)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    args.output_md.write_text(render_markdown(manifest), encoding="utf-8")
    print(f"Manifesto JSON: {args.output_json}")
    print(f"Inventário Markdown: {args.output_md}")
    print(f"Status: {manifest['status']}")
    return 1 if manifest["blocking_issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
