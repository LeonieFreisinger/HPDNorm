import argparse

from pipeline import synthetic_data
from pipeline.helpers.data_loaders import DATASETS
from pipeline.models import params_generators
from pipeline.models.models import SUPPORTED_MODELS
from pipeline.models.params import SUPPORTED_PARAMS


def get_synth_data_arg_parser():
    parser = argparse.ArgumentParser(description="Run a benchmark on synthetic data")
    parser.add_argument(
        "--data_func",
        type=str,
        required=False,
        default=None,
        help="Data function",
        choices=synthetic_data.__all__,
    )
    parser.add_argument(
        "--data_n_ts_groups",
        type=str,
        required=False,
        default="1,1",
        help="Number of timer series per group in data function",
    )
    parser.add_argument(
        "--data_offset_per_group",
        type=str,
        required=False,
        default="0,0",
        help="Offsets per group in data function",
    )
    parser.add_argument(
        "--data_amplitude_per_group",
        type=str,
        required=False,
        default="0,0",
        help="Amplitudes per group in data function",
    )
    parser.add_argument(
        "--data_trend_gradient_per_group",
        type=str,
        required=False,
        default=None,
        help="Optional argument - Trend gradient per group in data ",
    )
    parser.add_argument(
        "--proportion_break",
        type=str,
        required=False,
        default=None,
        help="Optional argument - Proportion of breaks in data function",
    )
    parser.add_argument(
        "--heterogeneity_type",
        type=str,
        required=False,
        default="amplitude",
        help="Heterogeneity type",
        choices=["amplitude", "offset", "trend", "heteroscedacity", "structural_break"],
    )
    parser.add_argument(
        "--sample_upper_limit",
        type=float,
        required=False,
        default="1.0",
        help="Upper limit of sampling range.",
    )

    add_common_args(parser)
    return parser.parse_args()


def get_real_data_arg_parser():
    parser = argparse.ArgumentParser(description="Run a benchmark on real data")
    parser.add_argument(
        "--dataset", type=str, required=True, help="Dataset", choices=DATASETS.keys()
    )
    parser.add_argument("--data_path", type=str, required=False, help="Dataset path")
    add_common_args(parser)
    return parser.parse_args()


def add_common_args(parser):
    parser.add_argument(
        "--model", type=str, required=True, help="Model class", choices=SUPPORTED_MODELS
    )
    parser.add_argument(
        "--params",
        type=str,
        required=True,
        help="Model parameters",
        choices=SUPPORTED_PARAMS,
    )
    parser.add_argument(
        "--gen_func",
        type=str,
        required=False,
        default="gen_model_and_params_default",
        help="Param generation function",
        choices=params_generators.__all__,
    )
    parser.add_argument(
        "--with_scalers",
        type=bool,
        required=False,
        default=False,
        help="Scaling",
    )
