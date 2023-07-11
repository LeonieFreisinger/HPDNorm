import os
import pathlib

import pandas as pd

from evaluation.baseline_forecasts.metric_caluclator import \
    calc_per_series_metrics
from evaluation.baseline_forecasts.params import get_exp_params
from evaluation.baseline_forecasts.parser import (extract_args_from_name,
                                                  parse_synthetic_data_files)
from pipeline.synthetic_data.base_generator import generate

parent_dir = pathlib.Path(__file__).parent.absolute()
tables_dir = os.path.join(parent_dir, "evaluation", "tables")
file_name_sampled_csv = os.path.join(tables_dir, "df_ideal_metrics_sampled.csv")
file_name_custom_csv = os.path.join(tables_dir, "df_ideal_metrics_custom.csv")

CUSTOM = False
SAMPLED = True
freq = "H"
series_length = 24 * 7 * 15
series_start = pd.to_datetime("2011-01-01 01:00:00")

if SAMPLED:
    synthetic_data_dfs = parse_synthetic_data_files()
    metric_results = pd.DataFrame()
    for exp_name, df in synthetic_data_dfs.items():
        metric_df = pd.DataFrame()
        metric_df = calc_per_series_metrics(df, ["MAE", "RMSE"])
        metric_df["exp_id"] = str(exp_name)
        metric_results = pd.concat(
            [metric_results, metric_df], ignore_index=True, axis=0
        )
    metric_results = metric_results.set_index(["exp_id", "ID"])
    # metric_results.columns = pd.MultiIndex.from_product([["baseline"], metric_results.columns])
    metric_results.to_csv(file_name_sampled_csv, index=True)


if CUSTOM:
    EXPERIMENT_NAMES_CUSTOM = get_exp_params()
    input_args_custom = list(map(extract_args_from_name, EXPERIMENT_NAMES_CUSTOM))
    common_args = {
        "series_start": series_start,
        "series_length": series_length,
        "freq": freq,
        "calc_without_noise": True,
    }
    input_args_with_common = [dict(arg_dict, **common_args) for arg_dict in input_args]
    synthetic_data_dfs = [generate(**arg_dict) for arg_dict in input_args_with_common]
    metric_results = pd.DataFrame()
    for i, df in enumerate(synthetic_data_dfs):
        metric_df = pd.DataFrame()
        metric_df = calc_per_series_metrics(df, ["MAE", "RMSE"])
        metric_df["exp_id"] = str(EXPERIMENT_NAMES_CUSTOM[i])
        metric_results = metric_results.append(metric_df, ignore_index=True)
    metric_results = metric_results.set_index(["exp_id", "ID"])
    metric_results.columns = pd.MultiIndex.from_product(
        [["exp_id"], metric_results.columns]
    )
    metric_results.to_csv(file_name_custom_csv, index=True)
