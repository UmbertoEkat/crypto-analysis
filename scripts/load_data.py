"""Load and prepare Binance OHLCV data from CSV files."""

import pandas as pd
from pathlib import Path

DATA = (Path(__file__).parents[2] / "DATA").resolve()


def load(file: str | Path, asset: str = "") -> pd.DataFrame:
    """Load 5m OHLCV BTC/PAXG data from a CSV file.

    Returns DataFrame with date index (UTC+8) and OHLCV columns.
    """
    df = pd.read_csv(
        file,
        usecols=["open_time", "open", "high", "low", "close", "volume"],
        parse_dates=["open_time"],
    )
    df = df.rename(columns={"open_time": "date"}).set_index("date").sort_index()
    return df


def btc() -> pd.DataFrame:
    return load(DATA / "BTCUSDT_5m_updated.csv", "BTC")


def paxg() -> pd.DataFrame:
    return load(DATA / "PAXGUSDT_5m_updated.csv", "PAXG")


def resample(df: pd.DataFrame, freq: str = "1h") -> pd.DataFrame:
    """Aggregate to higher timeframe."""
    return df.resample(freq).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }).dropna()
