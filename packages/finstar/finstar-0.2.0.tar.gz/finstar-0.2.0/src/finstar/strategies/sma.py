import numpy as np
import pandas as pd


def sma(series: pd.Series, short_period: int, long_period: int) -> pd.Series:
    short_series = series.rolling(short_period).mean()
    long_series = series.rolling(long_period).mean()
    sma_positions = pd.Series(
        np.where(short_series > long_series, 1, -1), index=series.index
    )
    # set nan values manually as > above concerts them to bool
    nans = np.logical_or(short_series.isna(), long_series.isna())
    sma_positions.loc[nans] = np.nan
    return sma_positions
