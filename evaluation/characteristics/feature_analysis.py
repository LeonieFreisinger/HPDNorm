import os
import pathlib
from typing import Dict, Union

import numpy as np
import pandas as pd
import tsfeatures
from statsmodels.tsa.seasonal import STL, seasonal_decompose

from evaluation.baseline_forecasts.parser import (extract_args_from_name,
                                                  parse_synthetic_data_files)
from pipeline.helpers.data_loaders import load_Australian, load_EIA, load_London, load_ERCOT, load_ETTh, load_Solar


# basic functions
def get_var(uni_ts: Union[pd.Series, np.ndarray]) -> np.float64:
    """
    :return: The variance of a given univariate time series.
    """
    return np.float64(np.var(uni_ts))


def get_mean(uni_ts: Union[pd.Series, np.ndarray]) -> np.float64:
    """
    :return: The arithmetic mean value of a given univariate time series.
    """
    return np.float64(np.mean(uni_ts))


def get_lumpiness(uni_ts: Union[pd.Series, np.ndarray]) -> np.float64:
    """
    :return: The lumpiness of a given univariate time series.
    """
    return np.float64(tsfeatures.lumpiness(uni_ts)["lumpiness"])


def get_stability(uni_ts: Union[pd.Series, np.ndarray]) -> np.float64:
    """
    :return: The stability of a given univariate time series.
    """
    return np.float64(tsfeatures.stability(uni_ts)["stability"])


def get_max_level_shift(uni_ts: Union[pd.Series, np.ndarray]) -> np.float64:
    """
    :return: The max level shift of a given univariate time series.
    """
    return np.float64(max_level_shift(uni_ts)["max_level_shift"])


def get_max_var_shift(uni_ts: Union[pd.Series, np.ndarray]) -> np.float64:
    """
    :return: The max var shift of a given univariate time series.
    """
    return np.float64(max_var_shift(uni_ts)["max_var_shift"])


# ST Decomposition
def _get_STL_components(series: pd.Series, seasonal: int, period: int):
    res = STL(series, seasonal=seasonal, period=period).fit()
    # res = seasonal_decompose(series, model='additive', filt=None, period=24, two_sided=True, extrapolate_trend=0)
    # res.plot().show()
    return res.trend, res.seasonal, res.resid


# trend strength
def get_trend_strength(series: pd.Series) -> np.float64:
    """
    :return: The trend strength of a given univariate time series.
    """
    # trend, seasonal, resid = _get_STL_components(series ,seasonal=13,period=24)
    # var_resid = get_var(resid)
    # var_trend_residuals = get_var(np.add(trend, resid))
    # return np.float64(max(0,(1-np.divide( var_resid, var_trend_residuals))))
    # Alternative to use tsfeatures instead of STL
    stl_features = tsfeatures.stl_features(series, 24)
    return stl_features["trend"]


def get_season_strength(series: pd.Series) -> np.float64:
    """
    :return: The seasonal strength of a given univariate time series.
    """
    # trend, seasonal, resid = _get_STL_components(series ,seasonal=13,period=24)
    # var_resid = get_var(resid)
    # var_trend_residuals = get_var(np.add(trend, resid))
    # return np.float64(max(0,(1-np.divide( var_resid, var_trend_residuals))))
    # Alternative to use tsfeatures instead of STL
    stl_features = tsfeatures.stl_features(series, 24)
    return stl_features["seasonal_strength"]


# weighted variance
def get_trend_free_variance(series: pd.Series) -> np.float64:
    trend, seasonal, resid = _get_STL_components(series, seasonal=13, period=24)
    var_resid = get_var(resid + seasonal)
    # add weight
    return np.float64(var_resid)

def get_trend_free_mean(series: pd.Series) -> np.float64:
    trend, seasonal, resid = _get_STL_components(series, seasonal=13, period=24)
    mean_resid = get_mean(resid + seasonal)
    return np.float64(mean_resid)

# weighted lumpiness
def get_trend_free_lumpiness(series: pd.Series) -> np.float64:
    trend, seasonal, resid = _get_STL_components(series, seasonal=13, period=24)
    # lumpiness_resid = get_lumpiness(resid + seasonal)
    lumpiness_resid = get_lumpiness(resid)
    # add weight
    return np.float64(lumpiness_resid)


def max_level_shift(series: pd.Series, width: int = 10) -> Dict[str, Union[float, int]]:
    try:
        rollmean = series.rolling(window=width, min_periods=1).mean()
    except Exception as e:
        print(f"Error: {e}")
        maxmeans = np.nan
        maxidx = np.nan
    else:
        means = np.abs(np.diff(rollmean))
        if len(means) == 0:
            maxmeans = 0
            maxidx = np.nan
        elif np.all(np.isnan(means)):
            maxmeans = np.nan
            maxidx = np.nan
        else:
            maxmeans = np.nanmax(means)
            maxidx = np.nanargmax(means) + width - 1

    return {"max_level_shift": maxmeans, "time_level_shift": maxidx}


def max_var_shift(series: pd.Series, width: int = 10) -> Dict[str, Union[float, int]]:
    try:
        rollvar = series.rolling(window=width, min_periods=1).var()
    except Exception as e:
        print(f"Error: {e}")
        maxvar = np.nan
        maxidx = np.nan
    else:
        vars = np.abs(np.diff(rollvar))
        if len(vars) == 0:
            maxvar = 0.0
            maxidx = np.nan
        elif np.all(np.isnan(vars)):
            maxvar = np.nan
            maxidx = np.nan
        else:
            maxvar = np.nanmax(vars)
            maxidx = np.nanargmax(vars) + width - 1

    return {"max_var_shift": maxvar, "time_var_shift": maxidx}


def calculate_per_series_features(
    df_mvts: pd.DataFrame, features_list: list
) -> pd.DataFrame:
    """
    This method computes a list of F statistical features on the given multivariate time series
    """
    df_features = pd.DataFrame(
        columns=[i.__name__.replace("get_", "") for i in features_list], dtype=float
    )
    for feature in features_list:
        feature_name = feature.__name__.replace("get_", "")
        df_extracted_feature = feature(df_mvts)
        df_features.loc[0, feature_name] = df_extracted_feature
    return df_features


def calulate_per_dataset_features(
    df: pd.DataFrame, features_list: list
) -> pd.DataFrame:
    per_series_features = df.groupby("ID").apply(
        lambda x: calculate_per_series_features(x["y"], features_list=features_list)
    )
    per_dataset_features_mean = per_series_features.groupby(level=1).mean()
    per_dataset_features_std = per_series_features.groupby(level=1).std()
    per_dataset_features = pd.concat(
        [per_dataset_features_mean, per_dataset_features_std],
        axis=1,
        keys=["mean", "std"],
    )
    return per_dataset_features


def calulate_per_dataset_features_for_df_dict(
    df_dict: dict, features_list: list
) -> pd.DataFrame:
    dfs_per_dataset_features = pd.DataFrame()
    for key, df in df_dict.items():
        df_per_dataset_features = calulate_per_dataset_features(
            df, features_list=features_list
        )
        df_per_dataset_features.index = [key]
        dfs_per_dataset_features = pd.concat(
            [dfs_per_dataset_features, df_per_dataset_features], axis=0
        )

    return dfs_per_dataset_features


def exe_calulate_features_synthetic_data():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    df_dict_synthetic_data = parse_synthetic_data_files()
    list = [
        # get_max_level_shift,
        # get_max_var_shift,
        # get_trend_strength,
        # get_season_strength,
        # get_trend_free_variance,
        # get_trend_free_lumpiness,
        # get_stability,
        get_mean,
        # get_trend_free_variance,
    ]
    all_per_dataset_features = calulate_per_dataset_features_for_df_dict(
        df_dict_synthetic_data, features_list=list
    )
    print(all_per_dataset_features)

    all_per_dataset_features.to_csv(
        os.path.join(tables_dir, "all_per_dataset_features_synthetic.csv")
    )
    all_per_dataset_features.to_excel(os.path.join("all_per_dataset_features_synthetic.xlsx"))

def exe_calulate_features_real_world_data():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    # dataset_dir = os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "datasets")
    df_dict_synthetic_data = {
        'Australian': load_Australian(),
        'EIA': load_EIA(),
        'London': load_London(),
        'ERCOT': load_ERCOT(),
        'ETTh': load_ETTh(),
        'Solar': load_Solar(),
    }
    list = [
        # get_max_level_shift,
        # get_max_var_shift,
        # get_trend_strength,
        # get_season_strength,
        # get_trend_free_variance,
        # get_trend_free_lumpiness,
        # get_stability,
        get_mean
    ]
    all_per_dataset_features = calulate_per_dataset_features_for_df_dict(
        df_dict_synthetic_data, features_list=list
    )
    print(all_per_dataset_features)

    all_per_dataset_features.to_csv(
        os.path.join(tables_dir, "all_per_dataset_features_real_world.csv")
    )
    all_per_dataset_features.to_excel(os.path.join("all_per_dataset_features_real_world.xlsx"))
