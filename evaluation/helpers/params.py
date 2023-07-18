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


def get_het_type_order():
    return HET_TYPE_ORDER


def get_full_model_names():
    return FULL_MODEL_NAMES


def get_full_het_names():
    return FULL_HET_NAMES


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

FULL_MODEL_NAMES = {
    "TP_localST": "TorchProphet (local S & T)",
    "NP_localST": "NeuralProphet (local S & T)",
    "TP": "TorchProphet",
    "NP": "NeuralProphet",
    "NP_FNN": "LinearRegression",
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
    "structural_break": "Strcutural Break",
}
