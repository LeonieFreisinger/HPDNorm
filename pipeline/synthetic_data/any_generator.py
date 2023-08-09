import numpy as np
import pandas as pd
from statsmodels.tsa.arima_process import ArmaProcess

from evaluation.baseline_forecasts.ar_series_calculator import calc_ar_series


def create_time_series_data(
    series_length,
    amplitude=1,
    offset=0,
    trend_gradient=1,
    heteroscedasticity_strength=1,
    structural_break_variance=1,
    structural_break_mean=0,
    calc_without_noise=False,
):
    proportion_season = 2
    proportion_ar = 1
    proportion_noise = 0.5

    t = np.arange(series_length)
    period = 24
    omega = 2 * np.pi / period
    ar_coeffs = np.array([1, 0.5, -0.1, 0.02, 0.3])
    ma_coeffs = np.array([1])  # MA coefficients (no MA component)
    ar_process = ArmaProcess(ar_coeffs, ma_coeffs, nobs=series_length)

    season_group = (
        np.sin(omega * t)
        + np.cos(omega * t)
        + np.sin(2 * omega * t)
        + np.cos(2 * omega * t)
    )
    ar_group = ar_process.generate_sample(series_length)
    if calc_without_noise:
        # generate ideal ar_group without noise
        ar_group_without_noise = calc_ar_series(ar_group, ar_coeffs)

    trend = np.linspace(0, trend_gradient * 2, series_length)
    noise_group = np.random.normal(loc=0, scale=1, size=series_length)  # * trend
    heteroscedasticity = (
        np.linspace(1, heteroscedasticity_strength + 1, series_length)
        if heteroscedasticity_strength > 0
        else 1
    )

    base_component_unscaled = (
        proportion_season * season_group
        + proportion_ar * ar_group
        + proportion_noise * noise_group
    )
    mean = np.mean(base_component_unscaled)
    std_dev = np.std(base_component_unscaled)
    base_component = (base_component_unscaled - mean) / std_dev
    type_specific_component = (
        base_component * amplitude * (heteroscedasticity) + offset + trend
    )
    type_specific_component[series_length // 2 :] *= structural_break_variance
    type_specific_component[series_length // 2 :] += structural_break_mean

    if calc_without_noise:
        # create combined data without noise
        base_component_without_noise_unscaled = (
            proportion_season * season_group + proportion_ar * ar_group_without_noise
        )
        base_component_without_noise = (
            base_component_without_noise_unscaled - mean
        ) / std_dev
        type_specific_component_ideal = (
            base_component_without_noise * amplitude * (heteroscedasticity)
            + offset
            + trend
        )
        type_specific_component_ideal[series_length // 2 :] *= structural_break_variance
        type_specific_component_ideal[series_length // 2 :] += structural_break_mean
        type_specific_component = np.vstack(
            (type_specific_component, type_specific_component_ideal)
        )

    return type_specific_component
