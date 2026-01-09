"""Data flow for legendary investors use case."""

from pathlib import Path

from crew.clients.equities import YFinanceEquityDataClient


def fetch_investor_data(
    tickers: list[str],
    raw_data_dir: Path,
    period: str = "1y",
) -> dict:
    """Fetch and cache price data for investor holdings."""
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    client = YFinanceEquityDataClient(raw_data_dir)
    frames = client.get_frames(tickers, period=period)
    return frames


if __name__ == "__main__":
    # For testing fetch independently
    from crew.legendary_investors.config import LegendaryInvestorsConfig

    config = LegendaryInvestorsConfig(name="legendary_investors")
    
    # Combine all unique tickers
    all_tickers = list(set(
        config.soros_holdings + 
        config.druckenmiller_holdings + 
        [config.benchmark]
    ))
    
    raw_dir = Path("resources") / "data" / "use_cases" / "legendary_investors" / "raw"
    print(f"Fetching data for {len(all_tickers)} tickers...")
    frames = fetch_investor_data(all_tickers, raw_dir, config.period)
    print(f"Fetched {len(frames)} ticker(s)")
