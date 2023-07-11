import numpy as np
import pandas as pd

from pipeline import synthetic_data
from pipeline.synthetic_data.any_generator import create_time_series_data


def generate(
    series_start,
    series_length,
    data_trend_gradient_per_group,
    data_func,
    n_ts_groups,
    offset_per_group,
    amplitude_per_group,
    proportion_break,
    freq,
):
    date_rng = pd.date_range(start=series_start, periods=series_length, freq=freq)
    if data_trend_gradient_per_group is not None:
        df = getattr(synthetic_data, data_func)(
            series_length=series_length,
            date_rng=date_rng,
            n_ts_groups=n_ts_groups,
            offset_per_group=offset_per_group,
            amplitude_per_group=amplitude_per_group,
            trend_gradient_per_group=data_trend_gradient_per_group,
        )
    elif proportion_break is not None:
        df = getattr(synthetic_data, data_func)(
            series_length=series_length,
            date_rng=date_rng,
            n_ts_groups=n_ts_groups,
            offset_per_group=offset_per_group,
            amplitude_per_group=amplitude_per_group,
            proportion_break=proportion_break,
        )
    else:
        df = getattr(synthetic_data, data_func)(
            series_length=series_length,
            date_rng=date_rng,
            n_ts_groups=n_ts_groups,
            offset_per_group=offset_per_group,
            amplitude_per_group=amplitude_per_group,
        )
    return df


def generate_any(
    series_start,
    series_length,
    freq,
    heterogeneity_type="amplitude",
    sample_upper_limit=1,
    calc_without_noise=False,
):
    date_rng = pd.date_range(start=series_start, periods=series_length, freq=freq)
    concatentated_df = pd.DataFrame()
    num_time_series = 10
    seeds = [22, 42, 17, 8, 9, 25, 27, 29, 31, 33]

    if heterogeneity_type == "amplitude":
        offset = 0
        trend_gradient = 0
        heteroscedasticity = 0
        structural_break_mean = 0
        structural_break_variance = 1
    if heterogeneity_type == "offset":
        amplitude = 1
        trend_gradient = 0
        heteroscedasticity = 0
        structural_break_mean = 0
        structural_break_variance = 1
    elif heterogeneity_type == "trend":
        offset = 0
        amplitude = 1
        heteroscedasticity = 0
        structural_break_mean = 0
        structural_break_variance = 1
    elif heterogeneity_type == "heteroscedasticity":
        offset = 0
        amplitude = 1
        trend_gradient = 0
        structural_break_mean = 0
        structural_break_variance = 1
    elif heterogeneity_type == "structural_break":
        offset = 0
        amplitude = 1
        trend_gradient = 0
        heteroscedasticity = 0

    for i in range(num_time_series):
        np.random.seed(seeds[i])
        if heterogeneity_type == "amplitude":
            amplitude = np.random.uniform(0, sample_upper_limit * 10) + 1
        if heterogeneity_type == "offset":
            offset = np.random.uniform(0, sample_upper_limit * 10 / 3)
        elif heterogeneity_type == "trend":
            trend_gradient = np.random.uniform(0, sample_upper_limit) + 2
        elif heterogeneity_type == "heteroscedasticity":
            heteroscedasticity = np.random.uniform(0, sample_upper_limit * 2) + 1
        elif heterogeneity_type == "structural_break":
            structural_break_mean = np.random.uniform(0, sample_upper_limit * 2) + 1
            structural_break_variance = np.random.uniform(0, sample_upper_limit) + 2

        time_series = create_time_series_data(
            series_length=series_length,
            amplitude=amplitude,
            offset=offset,
            trend_gradient=trend_gradient,
            heteroscedasticity_strength=heteroscedasticity,
            structural_break_variance=structural_break_variance,
            structural_break_mean=structural_break_mean,
            calc_without_noise=calc_without_noise,
        )
        df = pd.DataFrame(date_rng, columns=["ds"])
        df["y"] = time_series[0, :] if calc_without_noise else time_series
        df["ID"] = str(i)
        if calc_without_noise:
            df["y_ideal"] = time_series[1, :]

        concatentated_df = pd.concat([concatentated_df, df], axis=0).reset_index(
            drop=True
        )

    noise_term_std = concatentated_df.groupby("ID").apply(
        lambda x: (x["y"] - x["y_ideal"]).std()
    )
    noise_term_means = concatentated_df.groupby("ID").apply(
        lambda x: (x["y"] - x["y_ideal"]).mean()
    )
    averaged_std_noise_term = noise_term_std.mean()
    averaged_mean_noise_term = noise_term_means.mean()
    concatentated_df["y"] = (
        concatentated_df["y"] - averaged_mean_noise_term
    ) / averaged_std_noise_term
    concatentated_df["y_ideal"] = (
        concatentated_df["y_ideal"] - averaged_mean_noise_term
    ) / averaged_std_noise_term

    return concatentated_df
