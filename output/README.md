# Output Artifacts

This directory holds generated reports, markdown summaries, and serialized metrics created by backtests or use case runs.

## Common Subdirectories
- `backtests/` – human-readable reports produced by scripted backtest runs.
- `use_cases/` – ad-hoc executions triggered through `use_case_runner`.
- Additional timestamped folders may be created during experiments; keep them if they provide audit value.

## Housekeeping
- Do not edit generated files manually; re-run the appropriate script instead.
- Remove large or obsolete experiment folders before committing unless they are required for documentation or regression tests.
