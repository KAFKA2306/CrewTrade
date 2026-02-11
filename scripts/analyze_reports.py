import os
import re
base_dir = "/home/kafka/projects/crewTrade/output/backtests/securities_collateral_loan"
years = range(2021, 2026)
results = []
def parse_report(year):
    path = os.path.join(base_dir, f"{year}0531", "securities_collateral_loan_report.md")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        content = f.read()
    forward_return_match = re.search(
        r"\|\s*Annualized Return\s*\|\s*([\-\d\.]+)%", content
    )
    forward_return = (
        float(forward_return_match.group(1)) if forward_return_match else None
    )
    backtest_return_match = re.search(
        r"\|\s*Annual Return\s*\|\s*([\-\d\.]+)%", content
    )
    backtest_return = (
        float(backtest_return_match.group(1)) if backtest_return_match else None
    )
    holdings = {}
    backtest_sharpe_match = re.search(
        r"\|\s*Sharpe Ratio\s*\|\s*([\-\d\.]+)\s*\|", content
    )
    backtest_sharpe = (
        float(backtest_sharpe_match.group(1)) if backtest_sharpe_match else None
    )
    forward_vol_match = re.search(
        r"\|\s*Annualized Volatility\s*\|\s*([\-\d\.]+)%", content
    )
    forward_vol = float(forward_vol_match.group(1)) if forward_vol_match else None
    if "Max Sharpe Portfolio Holdings" in content:
        lines = content.split("\n")
        in_table = False
        for line in lines:
            if "Max Sharpe Portfolio Holdings" in line:
                in_table = True
                continue
            if in_table and line.strip().startswith("|") and "Ticker" in line:
                continue
            if in_table and line.strip().startswith("|") and "---" in line:
                continue
            if in_table and line.strip() == "":
                in_table = False
                continue
            if in_table and line.strip().startswith("|"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 7:
                    ticker = parts[1]
                    if ".T" in ticker:
                        weight_str = parts[2].replace("%", "")
                        name = parts[6]
                        try:
                            holdings[ticker] = {
                                "weight": float(weight_str),
                                "name": name,
                            }
                        except ValueError:
                            pass
    return {
        "year": year,
        "forward_return": forward_return,
        "backtest_return": backtest_return,
        "backtest_sharpe": backtest_sharpe,
        "forward_vol": forward_vol,
        "holdings": holdings,
    }
data = []
for y in years:
    res = parse_report(y)
    if res:
        data.append(res)
print("Year | IS Sharpe (Exp) | OOS Return | OOS Vol | OOS Sharpe (Real) | Degradation")
print("--- | --- | --- | --- | --- | ---")
for d in data:
    is_sharpe = d["backtest_sharpe"]
    oos_ret = d["forward_return"]
    oos_vol = d["forward_vol"]
    if oos_ret is not None and oos_vol is not None and oos_vol > 0:
        oos_sharpe = oos_ret / oos_vol
    else:
        oos_sharpe = 0.0
    degradation = oos_sharpe - is_sharpe if is_sharpe else 0
    print(
        f"{d['year']} | {is_sharpe:.3f} | {oos_ret}% | {oos_vol}% | {oos_sharpe:.3f} | {degradation:.3f}"
    )
print("\nTurnover Analysis:")
for i in range(1, len(data)):
    prev = data[i - 1]
    curr = data[i]
    all_tickers = set(prev["holdings"].keys()) | set(curr["holdings"].keys())
    turnover_sum = 0
    diffs = []
    for t in all_tickers:
        w_prev = prev["holdings"].get(t, {}).get("weight", 0)
        w_curr = curr["holdings"].get(t, {}).get("weight", 0)
        name = curr["holdings"].get(t, {}).get("name") or prev["holdings"].get(
            t, {}
        ).get("name", "Unknown")
        diff = w_curr - w_prev
        turnover_sum += abs(diff)
        if abs(diff) > 5.0:
            diffs.append((t, name, diff))
    turnover = turnover_sum / 2
    print(f"\n{curr['year']}: {turnover:.2f}% turnover vs {prev['year']}")
    print("  Key Changes (> 5%):")
    diffs.sort(key=lambda x: x[2], reverse=True)
    for t, n, d in diffs:
        print(f"    {t} ({n}): {d:+.2f}%")
