import logging

log = logging.getLogger("evaluation")


def get_all_model_names():
    return ALL_MODEL_NAMES


def get_default_scaler():
    return DEFAULT_SCALER


def get_all_scaling_levels():
    return ALL_SCALING_LEVEL


def get_heterogeneity_groups():
    return HET_GROUPS


def get_het_strength():
    return HET_STRENGTH_LIST


def get_model_id_order():
    return MODEL_ID_ORDER


def get_all_model_params():
    return ALL_MODEL_PARAMS


def get_het_type_order():
    return HET_TYPE_ORDER


def get_full_model_names():
    return FULL_MODEL_NAMES


def get_full_het_names():
    return FULL_HET_NAMES

def get_full_dataset_names():
    return FULL_DATASET_NAMES

def get_full_norm_names():
    return FULL_NORM_NAMES

HET_STRENGTH_LIST = [
    "0.0",
    "1.0",
    "2.0",
    "3.0",
    "4.0",
    "5.0",
    "6.0",
    "7.0," "8.0",
    "9.0",
]

HET_GROUPS = ["amplitude", "offset", "trend", "heteroscedasticity", "structural_break"]
HET_TYPE_ORDER = HET_GROUPS

ALL_MODEL_NAMES = [
    "NeuralProphetModel",
    "TorchProphetModel",
    "RNNModel",
    "TransformerModel",
    "LightGBMModel",
    "NaiveModel",
    "SeasonalNaiveModel",
]

DEFAULT_SCALER = [
    "None",
    "StandardScaler",
    "MinMaxScalerfeature_range=-0.5 0.5",
    "MinMaxScaler",
    "RobustScalerquantile_range=5 95",
    "PowerTransformer",
    "QuantileTransformeroutput_distribution='normal'",
    "LogTransformer",
]

ALL_SCALING_LEVEL = [
    "per_time_series",
    "per_dataset",
    "per_time_series_none",  # temp
    "per_time_series_std",  # temp
]

MODEL_ID_ORDER = [
    "TP_localST",
    "NP_localST",
    "TP",
    "NP",
    "NP_FNN",
    "NP_FNN_sw",
    "RNN",
    "TF",
    "LGBM",
]
ALL_MODEL_PARAMS = [
    "TP_localST",
    "NP_localST",
    "TP",
    "NP_FNN_sw",
    "NP_FNN",
    "NP",
    "RNN",
    "TF",
    "LGBM",
    "SNaive",
    "Naive",
]

FULL_MODEL_NAMES = {
    "TP_localST": "ProphetLST",
    "NP_localST": "NeuralProphetLST",
    "TP": "Prophet",
    "NP": "NeuralProphet",
    "NP_FNN": "Linear Regression",
    "NP_FNN_sw": "FNN",
    "RNN": "RNN",
    "TF": "Transformer",
    "LGBM": "LightGBM",
}

FULL_HET_NAMES = {
    "amplitude": "Amplitude",
    "offset": "Offset",
    "trend": "Trend",
    "heteroscedasticity": "Heteroscedasticity",
    "structural_break": "Structural Break",
}
FULL_DATASET_NAMES = {
    "Australian": "Australian",
    "EIA": "EIA",
    "ERCOT": "ERCOT",
    "ETTh": "ETTh",
    "London": "Portugal",
    "Solar": "Solar",
}

FULL_NORM_NAMES = {
    "StandardScaler_per_time_series": "StandardScaler<sub>ts</sub>",
    "RobustScalerquantile_range=5 95_per_time_series": "RobustScaler<sub>ts</sub>",
    "RobustScaler_per_time_series": "RobustScaler<sub>ts</sub>",
    "MinMaxScaler_per_time_series": "MinMaxScaler<sub>ts</sub>",
    "PowerTransformer_per_time_series": "PowerTransform<sub>ts</sub>",
    "LogTransformer_per_time_series":"LogTransform<sub>ts</sub>",
    "revin_instance": "RevInstanceNorm",
    "StandardScaler_per_dataset": "StandardScaler<sub>d</sub>",
    "RobustScalerquantile_range=5 95_per_dataset": "RobustScaler<sub>d</sub>",
    "RobustScaler_per_dataset": "RobustScaler<sub>d</sub>",
    "MinMaxScaler_per_dataset": "MinMaxScaler<sub>d</sub>",
    "PowerTransformer_per_dataset": "PowerTransform<sub>d</sub>",
    "LogTransformer_per_dataset": "LogTransform<sub>d</sub>",
    "revin_batch": "RevBatchNorm",
}
