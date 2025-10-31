# Legacy Use Cases

This directory keeps the original `ai_trading_crew` sample use cases that predate the modular package now maintained under `AITradingCrew/`. The code here is retained for reference and regression comparisons.

## Typical Usage
- `ai_trading_crew/use_cases/` – legacy scenario definitions. You can import them by adding the repo root to `PYTHONPATH` and running `python -m ai_trading_crew.use_cases.<module>`.
- Inputs and outputs mirror the newer package but are intentionally frozen; avoid mixing these assets with the production `AITradingCrew/ai_trading_crew` modules.

## Contribution Notes
- Do not add new features here. Modern development belongs in `AITradingCrew/ai_trading_crew/`.
- If you update historical behavior for documentation purposes, note the change in the main `AGENTS.md` guide so other contributors understand the divergence.
