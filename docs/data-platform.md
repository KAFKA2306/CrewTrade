# CrewTrade canonical data platform

## Purpose

CrewTrade no longer treats each use case's downloaded file as an independent source of truth. The canonical data platform preserves the original response, a normalized analytical table, lineage, quality results, and ingestion-run status before any report or model consumes the data.

```text
Official API / governed private input
        ↓
raw/      immutable response bytes + SHA-256
        ↓
bronze/   normalized Parquet, partitioned by dataset/source/run
        ↓
catalog.duckdb
          ingestion_runs
          dataset_files
          quality_results
          bronze_<dataset> views
        ↓
use-case exports / quantitative analysis / public reports
```

The default local root is `data/platform/`. It can be overridden with `crew-data --root <path>` or by passing a persistent mounted path from Dagu, a container, or WSL.

## Storage contract

Every accepted batch must retain:

- source and dataset identifiers;
- retrieval time and canonical HTTPS source URL;
- raw response bytes and SHA-256;
- normalized Parquet rows;
- declared primary key;
- schema and source metadata;
- quality-check results;
- immutable run manifest.

A failed quality check aborts publication of that batch. Existing files are never silently overwritten because each write is partitioned by `run_id`.

## Automated primary sources

| Source | Datasets | Authentication | Notes |
| --- | --- | --- | --- |
| FRED / ALFRED | Credit OAS, nominal yields, real yields, breakeven inflation | `FRED_API_KEY` | Observations retain real-time start/end dates so revisions can be reconstructed. |
| U.S. Treasury | Daily par-yield curve | none | Official XML is normalized to observation date, tenor, value and curve type. |
| SEC EDGAR | Filing history and company facts | declared `SEC_USER_AGENT` | Requests are throttled below the SEC fair-access ceiling. Filing accession numbers and XBRL facts are point-in-time records. |

## Governed sources that must not be guessed

`config/data_platform.yaml` also registers sources that are public documents, licensed benchmarks, or private contracts. Their absence is represented as an explicit blocked or partial status rather than an invented value.

- fundnote Kaihou NAV and notices;
- JPX ETF product master and product terms;
- EDINET API v2 and XBRL filings;
- LBMA benchmark history;
- WSTS public releases and member data;
- private brokerage collateral contract and account state.

The registry records ownership, access mode, licence state, refresh policy, required fields, and the exact reason automation is blocked.

## Commands

```bash
uv sync
uv run crew-data validate-config
uv run pytest tests/data_platform -q

# No external credentials required
uv run crew-data sync --source governed_manual

# Full public-source sync
export FRED_API_KEY=...
export SEC_USER_AGENT='CrewTrade contact@example.com'
uv run crew-data sync \
  --source fred \
  --source treasury_yield_curve \
  --source sec_edgar \
  --source governed_manual

uv run crew-data status
uv run crew-data query 'select * from bronze_credit_oas order by observation_date desc limit 20'
```

Equivalent Task targets are `data:validate`, `data:test`, `data:sync`, `data:sync:public`, `data:sync:registry`, and `data:status`.

## Runtime ownership

The canonical production store should run on a persistent filesystem controlled by CrewTrade. GitHub Actions is used for contract tests and optional snapshot artifacts; an expiring Actions artifact is not the source of truth. A Dagu or local scheduled job should mount the persistent `DATA_PLATFORM_ROOT` and execute `task data:sync:public`.

## Migration rule

Legacy `data/<use_case>/` files and Yahoo-based clients remain temporarily available so current reports do not break. Migration proceeds dataset by dataset:

1. ingest the official source into the canonical platform;
2. compare canonical and legacy outputs for the same observation dates;
3. implement an explicit export/view for the use case;
4. switch the analysis to the canonical view;
5. delete the legacy downloader only after parity and provenance checks pass.

Credit and yield analyses must migrate first because their existing ETF-price proxies do not represent credit OAS or the Treasury term structure.

## Primary specifications

- FRED API overview: https://fred.stlouisfed.org/docs/api/fred/overview.html
- FRED observations and vintages: https://fred.stlouisfed.org/docs/api/fred/series_observations.html
- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- SEC automated access: https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
- EDINET API documentation: https://disclosure2dl.edinet-fsa.go.jp/guide/static/disclosure/WEEK0060.html
- U.S. Treasury interest-rate data: https://home.treasury.gov/resource-center/data-chart-center/interest-rates
- DuckDB Parquet querying: https://duckdb.org/docs/stable/data/parquet/overview
