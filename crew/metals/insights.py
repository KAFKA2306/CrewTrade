from typing import Dict, List
import pandas as pd
def build_insight_markdown(analysis_payload: Dict[str, pd.DataFrame]) -> str:
    edges = analysis_payload["edges"].copy()
    metrics = analysis_payload["metrics"].copy()
    edges["date"] = pd.to_datetime(edges["date"])
    edges["abs_gap_pct"] = edges["gap_pct"].abs()
    date_start = edges["date"].min()
    date_end = edges["date"].max()
    total_signals = len(edges)
    lines: List[str] = []
    lines.append("
    lines.append("")
    lines.append("
    lines.append(f"- Date range: {date_start.date()} to {date_end.date()}")
    lines.append(f"- Total signals: {total_signals}")
    lines.append("")
    signal_counts = edges.groupby("ticker").size().reset_index(name="signals")
    lines.append(
        _format_table(signal_counts, ["ticker", "signals"], ["Ticker", "Signals"])
    )
    lines.append("")
    lines.append("
    abs_stats = (
        edges.groupby("ticker")["abs_gap_pct"]
        .agg(["count", "mean", "median", "max"])
        .reset_index()
    )
    abs_stats = abs_stats.rename(
        columns={
            "count": "signals",
            "mean": "mean_abs_gap_pct",
            "median": "median_abs_gap_pct",
            "max": "max_abs_gap_pct",
        }
    )
    abs_stats["mean_abs_gap_pct"] = (abs_stats["mean_abs_gap_pct"] * 100).round(2)
    abs_stats["median_abs_gap_pct"] = (abs_stats["median_abs_gap_pct"] * 100).round(2)
    abs_stats["max_abs_gap_pct"] = (abs_stats["max_abs_gap_pct"] * 100).round(2)
    lines.append(
        _format_table(
            abs_stats,
            [
                "ticker",
                "signals",
                "mean_abs_gap_pct",
                "median_abs_gap_pct",
                "max_abs_gap_pct",
            ],
            ["Ticker", "Signals", "Mean %", "Median %", "Max %"],
        )
    )
    lines.append("")
    lines.append("
    last_90_start = edges["date"].max() - pd.Timedelta(days=90)
    recent = edges[edges["date"] >= last_90_start]
    if not recent.empty:
        recent_counts = recent.groupby("ticker").size().reset_index(name="signals")
        recent_mean = (
            recent.groupby("ticker")["abs_gap_pct"]
            .mean()
            .reset_index(name="mean_abs_gap_pct")
        )
        recent_mean["mean_abs_gap_pct"] = (recent_mean["mean_abs_gap_pct"] * 100).round(
            2
        )
        recent_stats = pd.merge(
            recent_counts, recent_mean, on="ticker", how="outer"
        ).fillna(0)
        lines.append(
            _format_table(
                recent_stats,
                ["ticker", "signals", "mean_abs_gap_pct"],
                ["Ticker", "Signals", "Mean %"],
            )
        )
    else:
        lines.append("No signals in the last 90 days.")
    lines.append("")
    lines.append("
    streak_summary = _compute_streak_summary(edges)
    lines.append(
        _format_table(
            streak_summary,
            ["ticker", "max_length", "streaks_ge_2", "streaks_ge_3"],
            ["Ticker", "Max Days", "Streaks ≥2", "Streaks ≥3"],
        )
    )
    lines.append("")
    lines.append("
    threshold_tables = _compute_reversion_tables(metrics)
    for threshold, table in threshold_tables.items():
        lines.append(f"
        if table.empty:
            lines.append("No reversion within data horizon.")
        else:
            lines.append(
                _format_table(
                    table,
                    ["ticker", "count", "mean", "median", "max"],
                    ["Ticker", "Count", "Mean Days", "Median Days", "Max Days"],
                )
            )
        lines.append("")
    lines.append("
    next_signal = _compute_next_signal_stats(edges)
    if next_signal.empty:
        lines.append("Not enough sequential signals per ticker.")
    else:
        lines.append(
            _format_table(
                next_signal,
                ["ticker", "median_days", "mean_change_pct"],
                ["Ticker", "Median Days", "Mean ΔGap %"],
            )
        )
    lines.append("")
    lines.append("
    threshold_tables = _compute_gap_threshold_stats(metrics)
    for threshold, table in threshold_tables.items():
        lines.append(f"
        if table.empty:
            lines.append("No qualifying events.")
        else:
            lines.append(
                _format_table(
                    table,
                    [
                        "ticker",
                        "events",
                        "successes",
                        "success_rate",
                        "mean_days",
                        "median_days",
                        "max_days",
                    ],
                    [
                        "Ticker",
                        "Events",
                        "Successes",
                        "Success %",
                        "Mean Days",
                        "Median Days",
                        "Max Days",
                    ],
                )
            )
        lines.append("")
    return "\n".join(lines)
def _format_table(df: pd.DataFrame, columns: List[str], headers: List[str]) -> str:
    table_lines: List[str] = []
    table_lines.append("| " + " | ".join(headers) + " |")
    table_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df[columns].iterrows():
        formatted = []
        for col in columns:
            value = row[col]
            if isinstance(value, float):
                formatted.append(f"{value:.2f}")
            else:
                formatted.append(str(value))
        table_lines.append("| " + " | ".join(formatted) + " |")
    return "\n".join(table_lines)
def _compute_streak_summary(edges: pd.DataFrame) -> pd.DataFrame:
    summary_records: List[Dict[str, object]] = []
    for ticker, group in edges.sort_values("date").groupby("ticker"):
        streak_lengths: List[int] = []
        streak_length = 0
        prev_date = None
        prev_direction = None
        for _, row in group.iterrows():
            current_date = row["date"]
            current_direction = row["direction"]
            if (
                prev_date is None
                or current_date != prev_date + pd.Timedelta(days=1)
                or current_direction != prev_direction
            ):
                if streak_length > 0:
                    streak_lengths.append(streak_length)
                streak_length = 1
            else:
                streak_length += 1
            prev_date = current_date
            prev_direction = current_direction
        if streak_length > 0:
            streak_lengths.append(streak_length)
        if not streak_lengths:
            summary_records.append(
                {
                    "ticker": ticker,
                    "max_length": 1,
                    "streaks_ge_2": 0,
                    "streaks_ge_3": 0,
                }
            )
        else:
            max_length = max(streak_lengths)
            streaks_ge_2 = sum(1 for length in streak_lengths if length >= 2)
            streaks_ge_3 = sum(1 for length in streak_lengths if length >= 3)
            summary_records.append(
                {
                    "ticker": ticker,
                    "max_length": max_length,
                    "streaks_ge_2": streaks_ge_2,
                    "streaks_ge_3": streaks_ge_3,
                }
            )
    return pd.DataFrame(summary_records)
def _compute_reversion_tables(metrics: pd.DataFrame) -> Dict[float, pd.DataFrame]:
    thresholds = [2.0, 1.5, 1.0, 0.5]
    records: List[Dict[str, object]] = []
    for ticker in metrics.columns.levels[0]:
        z_series = metrics[(ticker, "z_score")]
        z = z_series.reset_index()
        z.columns = ["date", "z"]
        z = z.dropna(subset=["z"])
        z["flag"] = z["z"].abs() >= 2.0
        flagged = z[z["flag"]]
        for idx, start_row in flagged.iterrows():
            future = z[z.index > idx]
            for threshold in thresholds:
                below = future[future["z"].abs() < threshold]
                if below.empty:
                    continue
                duration = int((below.iloc[0]["date"] - start_row["date"]).days)
                if duration >= 0:
                    records.append(
                        {"ticker": ticker, "threshold": threshold, "duration": duration}
                    )
    tables: Dict[float, pd.DataFrame] = {}
    reversion_df = pd.DataFrame(records)
    for threshold in thresholds:
        subset = reversion_df[reversion_df["threshold"] == threshold]
        if subset.empty:
            tables[threshold] = pd.DataFrame()
        else:
            stats = (
                subset.groupby("ticker")["duration"]
                .agg(["count", "mean", "median", "max"])
                .reset_index()
            )
            tables[threshold] = stats
    return tables
def _compute_next_signal_stats(edges: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for ticker, group in edges.sort_values("date").groupby("ticker"):
        seq = group.reset_index(drop=True)
        if len(seq) < 2:
            continue
        deltas: List[int] = []
        changes: List[float] = []
        for i in range(len(seq) - 1):
            delta_days = int((seq.loc[i + 1, "date"] - seq.loc[i, "date"]).days)
            change = float(seq.loc[i + 1, "abs_gap_pct"] - seq.loc[i, "abs_gap_pct"])
            deltas.append(delta_days)
            changes.append(change)
        if deltas:
            median_days = float(pd.Series(deltas).median())
            mean_change_pct = float(pd.Series(changes).mean() * 100)
            rows.append(
                {
                    "ticker": ticker,
                    "median_days": median_days,
                    "mean_change_pct": mean_change_pct,
                }
            )
    return pd.DataFrame(rows)
def _compute_gap_threshold_stats(metrics: pd.DataFrame) -> Dict[float, pd.DataFrame]:
    thresholds = [0.08, 0.10, 0.12]
    records: List[Dict[str, object]] = []
    for ticker in metrics.columns.levels[0]:
        ticker_frame = metrics[ticker][["gap_pct"]].dropna()
        ticker_frame = ticker_frame.sort_index()
        ticker_frame["abs_gap"] = ticker_frame["gap_pct"].abs()
        for threshold in thresholds:
            prev_abs = ticker_frame["abs_gap"].shift(1)
            trigger_mask = (ticker_frame["abs_gap"] >= threshold) & (
                (prev_abs < threshold) | prev_abs.isna()
            )
            trigger_dates = ticker_frame.index[trigger_mask]
            for trigger_date in trigger_dates:
                future = ticker_frame.loc[ticker_frame.index > trigger_date]
                target = future[future["abs_gap"] < threshold / 2]
                if not target.empty:
                    duration = int((target.index[0] - trigger_date).days)
                    success = 1
                else:
                    duration = None
                    success = 0
                records.append(
                    {
                        "ticker": ticker,
                        "threshold": threshold,
                        "events": 1,
                        "success": success,
                        "duration": duration,
                    }
                )
    df = pd.DataFrame(records)
    tables: Dict[float, pd.DataFrame] = {}
    for threshold in [0.08, 0.10, 0.12]:
        subset = df[df["threshold"] == threshold]
        if subset.empty:
            tables[threshold] = pd.DataFrame()
            continue
        summary = subset.groupby("ticker").agg(
            events=("events", "sum"), successes=("success", "sum")
        )
        durations = (
            subset[subset["duration"].notna()]
            .groupby("ticker")["duration"]
            .agg(["mean", "median", "max"])
        )
        table = summary.join(durations, how="left").fillna(0)
        table = table.reset_index()
        table["success_rate"] = (table["successes"] / table["events"] * 100).round(2)
        table["mean_days"] = table["mean"].round(2)
        table["median_days"] = table["median"].round(2)
        table["max_days"] = table["max"].astype(int)
        table = table.drop(columns=["mean", "median", "max"])
        tables[threshold] = table
    return tables
