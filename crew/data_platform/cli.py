from __future__ import annotations

import argparse
from pathlib import Path

import duckdb

from crew.data_platform.registry import load_config, sync


DEFAULT_CONFIG = Path("config/data_platform.yaml")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crew-data",
        description="CrewTrade canonical primary-data platform",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--root", type=Path, default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="Fetch and persist sources")
    sync_parser.add_argument(
        "--source",
        action="append",
        dest="sources",
        help="Source name from config/data_platform.yaml; repeatable",
    )

    subparsers.add_parser("status", help="Show recent ingestion runs and datasets")

    query_parser = subparsers.add_parser("query", help="Run a read-only DuckDB query")
    query_parser.add_argument("sql")

    subparsers.add_parser("validate-config", help="Validate configuration only")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    root = args.root or Path(config["storage"]["root"])

    if args.command == "validate-config":
        source_count = len(config.get("sources", {}))
        print(f"Config valid: schema_version=1, sources={source_count}, root={root}")
        return 0

    if args.command == "sync":
        run_id, persisted, manifest = sync(
            config_path=args.config,
            selected_sources=args.sources,
            root_override=args.root,
        )
        print(f"Run {run_id} succeeded: {len(persisted)} batches")
        for batch in persisted:
            print(
                f"- {batch.dataset}: rows={batch.row_count} "
                f"sha256={batch.raw_sha256[:16]} parquet={batch.parquet_path}"
            )
        print(f"Manifest: {manifest}")
        return 0

    catalog = root / "catalog.duckdb"
    if not catalog.exists():
        raise FileNotFoundError(
            f"Catalogue does not exist: {catalog}. Run `crew-data sync` first."
        )

    if args.command == "status":
        with duckdb.connect(str(catalog), read_only=True) as connection:
            runs = connection.execute(
                """
                SELECT run_id, started_at, completed_at, status, error
                FROM ingestion_runs
                ORDER BY started_at DESC
                LIMIT 20
                """
            ).fetchdf()
            datasets = connection.execute(
                """
                SELECT dataset, source, count(*) AS files, sum(row_count) AS rows,
                       max(retrieved_at) AS latest_retrieved_at
                FROM dataset_files
                GROUP BY dataset, source
                ORDER BY dataset, source
                """
            ).fetchdf()
        print("Recent runs")
        print(runs.to_string(index=False))
        print("\nDatasets")
        print(datasets.to_string(index=False))
        return 0

    if args.command == "query":
        sql = args.sql.strip()
        first_token = sql.split(maxsplit=1)[0].lower() if sql else ""
        if first_token not in {"select", "with", "show", "describe", "pragma"}:
            raise ValueError("Only read-only SQL is accepted by the CLI.")
        with duckdb.connect(str(catalog), read_only=True) as connection:
            result = connection.execute(sql).fetchdf()
        print(result.to_string(index=False))
        return 0

    raise AssertionError(f"Unhandled command: {args.command}")
