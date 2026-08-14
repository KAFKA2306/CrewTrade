# Tooling contract — 2026

Issue #34 の実repo監査に基づくquality-gate契約です。目的は新しいツールを増やすことではなく、同じ種類の検査に複数authorityを持たせず、localとCIの境界を一致させることです。

## Before

- Python project (`pyproject.toml`) は存在したが `uv.lock` が `.gitignore` され、CIの `uv sync` は依存解決を固定できていなかった。
- formatter / linter / static type checker の明示authorityがなかった。
- 外部 `config/data_platform.yaml` はYAMLとして読み込まれた後、top-level mappingとschema version程度しか構造検証していなかった。
- Pages / data-platform CIは有効だったが、local fast checkの正準入口がなかった。
- rootの `Kronos` はURLを持たないgitlinkとして残り、Actions checkout cleanupで `.gitmodules` URL欠落warningを発生させていた。現行code searchで参照はない。

## After: authority map

| Concern | Authority | Scope |
| --- | --- | --- |
| dependency resolution | uv + committed `uv.lock` | Python project全体 |
| format | Ruff 0.16.0 | maintained Python: `crew/data_platform`, `crew/yields`, `web`, `tests/data_platform` |
| lint | Ruff 0.16.0 | 同上 |
| static typing | Pyrefly 1.1.1 | fail-closed external config schema boundary |
| runtime boundary validation | Pydantic 2.x | `config/data_platform.yaml` only |
| local hook orchestration | prek 0.4.10 | `scripts/check.sh` |
| full data-platform contracts | pytest | existing `data-platform.yml` integration gate |
| static Pages build/audit | `scripts/check_pages.sh` | Pages/data-platform integration gate |

## Commands

Fresh clone bootstrap:

```bash
bash scripts/bootstrap.sh
```

Repository fast check:

```bash
bash scripts/check.sh
```

`prek` installs a single local hook that calls the same `scripts/check.sh`; CI does not maintain a second set of lint/type commands.

## Lock contract

`uv.lock` is committed. `scripts/check.sh` starts with:

```bash
uv lock --check
```

and subsequent project commands use `--locked`. A dependency edit without a matching lock update therefore fails before lint/type/tests are treated as valid.

## Why Pydantic is narrow

Pydantic is used only where untrusted YAML crosses into the application. `StorageConfig`, `SourceConfig`, and `DataPlatformConfig` validate the data-platform configuration before adapter construction. Existing internal `DatasetBatch`, `QualityCheck`, `PersistedBatch`, and `SourceAdapter` remain dataclass/Protocol contracts; converting pandas-heavy internal objects to Pydantic would add duplicate validation and serialization cost without creating a new trust boundary.

## Pyrefly staged scope

A first whole-repository Pyrefly run exposed 40 pre-existing errors, dominated by pandas typing/stub boundaries, dynamic source payloads, and script-style web imports. They are not hidden with blanket ignores and are not declared solved by this issue.

For this migration, Pyrefly is the sole static type authority for the newly hardened external configuration schema. Expanding the typed surface is a separate incremental task: a module enters the Pyrefly project only after its existing errors are fixed rather than suppressed.

## N/A tools

- **Biome / Oxlint / TypeScript / Zod:** maintained Pages UI is plain JavaScript without an npm dependency graph, TypeScript build, or bundler. Adding a second package ecosystem solely for tooling would increase authority count. Re-evaluate if the browser surface moves to TypeScript.
- **Nx / Turborepo:** CrewTrade is not a multi-project monorepo, so neither is installed.
- **Pydantic on internal pandas/domain objects:** not a trust boundary; intentionally not installed there.

## Migration evidence

The initial Ruff migration found formatting drift and 98 lint findings; 97 were resolved by Ruff safe fixes. The remaining `zip()` length contract in `crew/yields/allocation.py` was fixed explicitly with `strict=True`; unsafe Ruff fixes were not enabled.

The migration-only CI write path was removed before merge. Final `quality.yml` has `contents: read` and is fail-closed.

The stale `Kronos` gitlink was removed because it had no repository URL, no code references, and caused checkout cleanup warnings.

## Timing policy

There was no prior dedicated fast-quality workflow, so no artificial “speedup percentage” is claimed. The exact-head and exact-main Actions runs are the timing evidence. CrewTrade has a large existing dependency graph, so cold environment setup dominates the first run; cache behavior is reported separately from lint/type execution rather than using vendor benchmark claims.

## Primary documentation

- uv lock/sync: https://docs.astral.sh/uv/concepts/projects/sync/
- uv GitHub Actions: https://docs.astral.sh/uv/guides/integration/github/
- Ruff formatter: https://docs.astral.sh/ruff/formatter/
- Ruff linter: https://docs.astral.sh/ruff/linter/
- Pyrefly configuration: https://pyrefly.org/en/docs/configuration/
- Pydantic models: https://docs.pydantic.dev/latest/concepts/models/
- prek configuration: https://prek.j178.dev/configuration/
