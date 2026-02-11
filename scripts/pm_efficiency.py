import pandas as pd
def analyze_efficiency():
    filepath = "output/use_cases/precious_metals_spread/20251029/edge_insights.md"
    try:
        with open(filepath, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found {filepath}")
        return
    print("
    current_profit_est = 0.0
    results = []
    lines = content.splitlines()
    for line in lines:
        line = line.strip()
        if "≥ 8% → < 4%" in line:
            current_profit_est = 4.0
        elif "≥ 10% → < 5%" in line:
            current_profit_est = 5.0
        elif "≥ 12% → < 6%" in line:
            current_profit_est = 6.0
        if (
            "|" in line
            and "Ticker" not in line
            and "---" not in line
            and current_profit_est > 0
        ):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 5:
                ticker = parts[0]
                try:
                    mean_days = float(parts[4])
                except ValueError:
                    continue
                if mean_days > 0:
                    daily_roi_pct = current_profit_est / mean_days
                    ann_roi_pct = daily_roi_pct * 250
                    results.append(
                        {
                            "Scenario": f"Threshold {int(current_profit_est * 2)}%->{int(current_profit_est)}%",
                            "Ticker": ticker,
                            "Mean Days": mean_days,
                            "ROI/Day (%)": round(daily_roi_pct, 4),
                            "Ann. ROI (x250) (%)": round(ann_roi_pct, 1),
                        }
                    )
    if results:
        df = pd.DataFrame(results)
        df = df.sort_values("ROI/Day (%)", ascending=False)
        print(df.to_string(index=False))
    else:
        print("No efficiency data extracted. Check file format.")
if __name__ == "__main__":
    analyze_efficiency()
