import pandas as pd
from pathlib import Path
import yaml
from crew.securities_collateral_loan.config import (
    SecuritiesCollateralLoanConfig,
)
from crew.securities_collateral_loan.data_pipeline import (
    SecuritiesCollateralLoanDataPipeline,
)
from crew.securities_collateral_loan.analysis import (
    SecuritiesCollateralLoanAnalyzer,
)
from crew.securities_collateral_loan.reporting import (
    SecuritiesCollateralLoanReporter,
)

config_path = Path("config/use_cases/securities_collateral_loan.yaml")
with open(config_path) as f:
    config_dict = yaml.safe_load(f)

config = SecuritiesCollateralLoanConfig(**config_dict)

start_year = 2009
end_year = 2024
results = []

for year in range(start_year, end_year + 1):
    anchor_date = pd.Timestamp(f"{year}-05-31")
    date_str = anchor_date.strftime("%Y%m%d")

    print(f"\n{'=' * 60}")
    print(f"Running backtest for {date_str}")
    print(f"{'=' * 60}")

    raw_dir = Path("resources/data/use_cases/securities_collateral_loan/raw")
    processed_dir = Path(
        f"resources/data/use_cases/securities_collateral_loan/processed/{date_str}"
    )
    report_dir = Path(f"output/backtests/securities_collateral_loan/{date_str}")

    try:
        pipeline = SecuritiesCollateralLoanDataPipeline(config, raw_dir)
        analyzer = SecuritiesCollateralLoanAnalyzer(config)
        reporter = SecuritiesCollateralLoanReporter(config, processed_dir, report_dir)

        data_payload = pipeline.collect(as_of=anchor_date)

        if data_payload.get("mode") != "optimization":
            print("  SKIP: Not in optimization mode")
            continue

        if "prices" not in data_payload or data_payload["prices"].empty:
            print("  SKIP: No price data available")
            continue

        analysis_payload = analyzer.evaluate(data_payload)
        reporter.persist(analysis_payload)

        summary = analysis_payload["summary"]
        opt_metrics = analysis_payload.get("optimization_metrics", {})
        asset_breakdown = analysis_payload.get("asset_breakdown", pd.DataFrame())

        ltv = summary["current_loan_ratio"]
        ltv_ok = ltv <= config.ltv_limit

        portfolio_vol = opt_metrics.get("annual_volatility", 0)
        vol_ok = portfolio_vol <= 0.15

        max_category_weight = 0.0
        category_ok = True
        if "category" in asset_breakdown.columns:
            cat_weights = (
                asset_breakdown.groupby("category")["market_value"].sum()
                / asset_breakdown["market_value"].sum()
            )
            max_category_weight = float(cat_weights.max())
            category_ok = max_category_weight <= 0.5

        max_expense = 0.0
        expense_ok = True
        if "expense_ratio" in asset_breakdown.columns:
            valid_expenses = asset_breakdown["expense_ratio"].dropna()
            if not valid_expenses.empty:
                max_expense = float(valid_expenses.max())
                expense_ok = max_expense < 0.004

        all_ok = ltv_ok and vol_ok and category_ok and expense_ok

        result = {
            "year": year,
            "date": date_str,
            "ltv": float(ltv),
            "ltv_limit": config.ltv_limit,
            "ltv_ok": ltv_ok,
            "portfolio_vol": float(portfolio_vol),
            "vol_limit": 0.15,
            "vol_ok": vol_ok,
            "max_category_weight": float(max_category_weight),
            "category_limit": 0.5,
            "category_ok": category_ok,
            "max_expense": float(max_expense),
            "expense_limit": 0.004,
            "expense_ok": expense_ok,
            "all_constraints_ok": all_ok,
            "collateral_value": float(summary["current_collateral_value"]),
            "num_etfs": len(asset_breakdown),
            "sharpe_ratio": float(opt_metrics.get("sharpe_ratio", 0)),
            "annual_return": float(opt_metrics.get("annual_return", 0)),
        }

        results.append(result)

        status = "✅ PASS" if all_ok else "❌ FAIL"
        print(f"  {status}")
        print(f"    LTV: {ltv:.4f} {'✓' if ltv_ok else '✗'}")
        print(f"    Vol: {portfolio_vol:.4f} {'✓' if vol_ok else '✗'}")
        print(f"    Cat: {max_category_weight:.4f} {'✓' if category_ok else '✗'}")
        print(f"    Exp: {max_expense:.4f} {'✓' if expense_ok else '✗'}")

    except Exception as e:
        print(f"  ERROR: {str(e)}")
        results.append(
            {
                "year": year,
                "date": date_str,
                "error": str(e),
                "all_constraints_ok": False,
            }
        )

results_df = pd.DataFrame(results)
results_path = Path(
    "output/backtests/securities_collateral_loan/validation_results.csv"
)
results_path.parent.mkdir(parents=True, exist_ok=True)
results_df.to_csv(results_path, index=False)

print(f"\n{'=' * 60}")
print("SUMMARY")
print(f"{'=' * 60}")
print(f"Total years: {len(results)}")
passed = sum(1 for r in results if r.get("all_constraints_ok", False))
print(f"Passed: {passed}")
print(f"Failed: {len(results) - passed}")
print(f"\nResults saved to: {results_path}")
