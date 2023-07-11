import pandas as pd
from tot.evaluation.metrics import ERROR_FUNCTIONS


def calc_scaled_metric_avg(df, metrics):
    metrics_per_series = calc_per_series_metrics(df, metrics)
    metrics_per_dataset = metrics_per_series[metrics].mean(axis=0)
    return metrics_per_dataset


def calc_per_series_metrics(df, metrics):
    metrics_df = pd.concat(
        [
            df.groupby("ID").apply(
                lambda x: ERROR_FUNCTIONS[metric](
                    predictions=x["y_ideal"].values,
                    truth=x["y"].values,
                    freq="H",
                )
            )
            for metric in metrics
        ],
        axis=1,
        keys=metrics,
    )
    metrics_df = metrics_df.reset_index()
    return metrics_df
