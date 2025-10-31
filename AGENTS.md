# Repository Guidelines

## Project Structure & Module Organization
The Python package lives under `AITradingCrew/ai_trading_crew/`, with subpackages for `use_cases/`, `backtests/`, and shared utilities. Configuration defaults sit in `AITradingCrew/config/`, while reusable data caches are stored in `AITradingCrew/resources/data/`. Generated artifacts (reports, parquet outputs, diagnostics) are written to `AITradingCrew/output/` and `AITradingCrew/resources/data/.../processed_backtests/`. Keep ad-hoc experiments inside `tmp_*` folders or a dedicated branch; do not mix them with the shipped package.

## Build, Test, and Development Commands
- `uv sync` (or `poetry install`): create a Python 3.10+ environment with all project dependencies, including CrewAI.
- `PYTHONPATH=AITradingCrew python3 AITradingCrew/ai_trading_crew/backtests/securities_collateral_loan_backtest.py securities_collateral_loan --config AITradingCrew/config/use_cases/securities_collateral_loan.yaml`: regenerate historical and forward reports for the collateral-loan workflow.
- `python -m ai_trading_crew.use_case_runner securities_collateral_loan --config <path>`: run a single use case end-to-end, persisting outputs under `output/use_cases/`.
- `pytest` (when adding unit tests under `tests/`): run the automated suite locally before submitting a PR.

## Coding Style & Naming Conventions
Follow PEP 8 with four-space indentation and `black`-compatible formatting. Use `snake_case` for modules, functions, and variables; reserve `CamelCase` for classes and TypedDicts. Keep configuration keys lowercase with underscores, mirroring the patterns already in `config/use_cases/*.yaml`. Prefer explicit imports over wildcard usage, and co-locate helper functions within their owning module instead of adding new globals.

## Testing Guidelines
Validate data-processing changes by re-running the relevant backtest scripts and confirming new parquet outputs land in the `processed_backtests/<anchor>/` directory. When feasible, cover deterministic logic with `pytest` cases named `test_<feature>_behavior.py`. Include sample fixtures under `tests/fixtures/` and assert both expected metrics and schema compatibility. For new agents or pipelines, document manual verification steps in the PR description.

## Commit & Pull Request Guidelines
Write imperative, present-tense commit messages (e.g., `Add collateral optimizer score weighting`). Group related edits into a single commit where possible, and reference issue IDs using `Refs #123` in the footer. Pull requests should describe motivation, summarize key code paths touched, and link to generated reports (for example, `AITradingCrew/output/backtests/securities_collateral_loan/20250531/`). If UI or reporting artifacts change, attach screenshots or paste relevant metric tables. Request review from the domain owner responsible for the affected use case.

## Data & Credential Handling
Never commit `.env` files or API keys. Use the cached parquet data already tracked in `AITradingCrew/resources/data/` and document any new external datasets in the README plus `config/use_cases/`. When introducing new credentials, reference environment variables in code and update `.env.example` instead of hardcoding secrets.
