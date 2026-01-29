"""Data pipeline for semiconductor stock data fetching."""

from pathlib import Path

from crew.clients.equities import YFinanceEquityDataClient


def fetch_semiconductor_data(
    tickers: list[str],
    raw_data_dir: Path,
    period: str = "1y",
) -> dict:
    """Fetch and cache price data for semiconductor stocks."""
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    client = YFinanceEquityDataClient(raw_data_dir)
    frames = client.get_frames(tickers, period=period)
    return frames


if __name__ == "__main__":
    from pathlib import Path

    # Default tickers
    tickers = [
        "NVDA",
        "TSM",
        "AVGO",
        "ASML",
        "QCOM",
        "AMD",
        "INTC",
        "LRCX",
        "ADI",
        "MU",
        "SOXX",  # Benchmark
    ]

    raw_dir = Path("resources") / "data" / "use_cases" / "semiconductors" / "raw"
    print(f"Fetching data for {len(tickers)} tickers...")
    frames = fetch_semiconductor_data(tickers, raw_dir)
    print(f"Fetched {len(frames)} ticker(s)")
    for ticker, df in frames.items():
        print(f"  {ticker}: {len(df)} rows")
