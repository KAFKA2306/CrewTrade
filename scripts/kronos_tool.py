import os, sys, argparse
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import timedelta
from crew.utils.kronos_utils import get_kronos_forecast
def prepare_df(df):
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    df.columns = [str(c).lower() for c in df.columns]
    if 'close' not in df.columns and 'adj close' in df.columns: df['close'] = df['adj close']
    df = df.reset_index()
    if 'Date' not in df.columns: df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    return df
def run_forecast(ticker, label, backtest=False, pred_len=91):
    print(f"--- {label} ({ticker}) ---")
    df = yf.download(ticker, period='2y')
    if df.empty: return
    df = prepare_df(df)
    anchors = [len(df)-(pred_len+120), len(df)-(pred_len+60), len(df)-1] if backtest else [len(df)-1]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Date'], df['close'], label='Actual', color='black', alpha=0.3)
    for i, a_idx in enumerate(anchors):
        a_date = df['Date'].iloc[a_idx]
        pred = get_kronos_forecast(df.iloc[:a_idx+1], df['Date'].iloc[:a_idx+1], pd.Series([a_date + timedelta(days=j+1) for j in range(pred_len)]), pred_len)
        ax.plot([a_date + timedelta(days=j+1) for j in range(pred_len)], pred['close'], linestyle='--', label=f"From {a_date.date()}")
        ax.scatter(a_date, df['close'].iloc[a_idx], s=15)
    ax.set_title(f"Kronos-2: {label} ({ticker}) {'Backtest' if backtest else 'Forecast'}")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3); plt.tight_layout()
    os.makedirs('output/plots', exist_ok=True)
    path = f"output/plots/{ticker.replace('.','_')}_{'backtest' if backtest else 'forecast'}.png"
    plt.savefig(path); print(f"Saved: {path}"); plt.close()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tickers", nargs='+', default=["ORCL"])
    parser.add_argument("--backtest", action="store_true")
    args = parser.parse_args()
    for t in args.tickers: run_forecast(t, t, backtest=args.backtest)
