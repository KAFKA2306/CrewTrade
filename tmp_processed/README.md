# Temporary Processed Outputs

This folder receives parquet artifacts when you run local experiments outside the canonical `AITradingCrew/resources/data/.../processed_backtests/` tree.

## Typical Contents
- Portfolio breakdowns (`asset_breakdown.parquet`, `portfolio_value.parquet`)
- Risk metrics and candidate universes
- Forward performance series for quick inspection

## Cleanup Policy
- Treat these files as scratch space. Delete the folder after validating results or promote the run into `AITradingCrew/resources/data/...` if it should be version-controlled.
