from pathlib import Path
from typing import Any, Dict
import pandas as pd
class ImuraFundAnalyzer:
    def __init__(self, raw_data_dir: Path):
        self.raw_data_dir = raw_data_dir
    def analyze(self, data_payload: Dict[str, str]) -> Dict[str, Any]:
        dfs = {}
        for name, path in data_payload.items():
            df = pd.read_csv(path, parse_dates=["Date"]).set_index("Date").sort_index()
            df = df[~df.index.duplicated(keep="first")]
            dfs[name] = df["Price"]
        combined = pd.concat(dfs.values(), axis=1, keys=dfs.keys()).dropna()
        normalized = combined / combined.iloc[0] * 100
        daily_returns = combined.pct_change().dropna()
        total_return = (combined.iloc[-1] / combined.iloc[0]) - 1
        days = (combined.index[-1] - combined.index[0]).days
        years = days / 365.25
        cagr = (1 + total_return) ** (1 / years) - 1
        volatility = daily_returns.std() * (252**0.5)
        sharpe = cagr / volatility
        drawdown = (combined - combined.cummax()) / combined.cummax()
        max_drawdown = drawdown.min()
        metrics = {
            col: {
                "Total Return": total_return[col],
                "CAGR": cagr[col],
                "Volatility": volatility[col],
                "Sharpe": sharpe[col],
                "MaxDD": max_drawdown[col],
            }
            for col in combined.columns
        }
        return {
            "metrics": metrics,
            "period": {
                "start": combined.index[0],
                "end": combined.index[-1],
                "days": days,
            },
            "combined_data": combined,
            "normalized_data": normalized,
            "drawdown_data": drawdown,
        }
if __name__ == "__main__":
    import datetime
    import yaml
    from crew.imura.reporting import ImuraFundReporter
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "imura.yaml"
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    targets = config.get("targets", {})
    raw_data_dir = PROJECT_ROOT / "data" / "imura"
    today = datetime.date.today().strftime("%SAME%m%d")
    report_dir = PROJECT_ROOT / "output" / "use_cases" / "imura" / today
    data_payload = {name: str(raw_data_dir / f"{name}.csv") for name in targets.keys()}
    analyzer = ImuraFundAnalyzer(raw_data_dir)
    analysis = analyzer.analyze(data_payload)
    reporter = ImuraFundReporter(report_dir)
    result = reporter.produce_report(analysis)
    print(f"Report saved: {result['report_file']}")
