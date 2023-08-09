import multiprocessing
import os
import pathlib as pathlib
import time

import numpy as np
import pandas as pd

from pipeline.helpers.arg_parsers import get_synth_data_arg_parser
from pipeline.helpers.misc import build_synth_data_name
from pipeline.pipeline import Pipeline
from pipeline.synthetic_data.base_generator import generate, generate_any

if __name__ == "__main__":
    args = get_synth_data_arg_parser()
    # save path
    base_dir_name = pathlib.Path(__file__).parent.absolute()
    result_dir_name = os.path.join(base_dir_name, "results")

    # Freezing support for multiprocessing
    multiprocessing.freeze_support()

    # post-processing args
    data_func = args.data_func
    if data_func is None:
        heterogeneity_type = str(args.heterogeneity_type)
        sample_upper_limit = float(args.sample_upper_limit)
    else:
        data_n_ts_groups = [int(i) for i in args.data_n_ts_groups.split(",")]
        data_offset_per_group = [int(i) for i in args.data_offset_per_group.split(",")]
        data_amplitude_per_group = [
            int(i) for i in args.data_amplitude_per_group.split(",")
        ]
        data_trend_gradient_per_group = (
            [float(i) for i in args.data_trend_gradient_per_group.split(",")]
            if args.data_trend_gradient_per_group is not None
            else None
        )
        proportion_break = (
            [int(i) for i in args.proportion_break.split(",")]
            if args.proportion_break is not None
            else None
        )

    freq = "H"
    series_length = 24 * 7 * 15
    series_start = pd.to_datetime("2011-01-01 01:00:00")

    if data_func is None:
        df = generate_any(
            series_start=series_start,
            series_length=series_length,
            freq=freq,
            heterogeneity_type=heterogeneity_type,
            sample_upper_limit=sample_upper_limit,
            calc_without_noise=True,
        )

        pipeline_name = build_synth_data_name(
            data_func=data_func,
            params_name=args.params,
            heterogeneity_type=heterogeneity_type,
            sample_upper_limit=sample_upper_limit,
        )
        # save ideal forecast
        folder_path = os.path.join(result_dir_name, pipeline_name)
        file_name = os.path.join(folder_path, "data.csv")

        try:
            os.mkdir(folder_path)
        except OSError as e:
            print(e)
        df.to_csv(file_name, index=False)
        df = df.drop("y_ideal", axis=1)

    else:
        df = generate(
            series_start=series_start,
            series_length=series_length,
            data_trend_gradient_per_group=data_trend_gradient_per_group,
            data_func=args.data_func,
            n_ts_groups=data_n_ts_groups,
            offset_per_group=data_offset_per_group,
            amplitude_per_group=data_amplitude_per_group,
            proportion_break=proportion_break,
            freq=freq,
        )

        pipeline_name = build_synth_data_name(
            data_func=data_func,
            params_name=args.params,
            n_ts_groups=data_n_ts_groups,
            amplitude_per_group=data_amplitude_per_group,
            offset_per_group=data_offset_per_group,
            trend_gradient_per_group=data_trend_gradient_per_group,
            proportion_break=proportion_break,
        )

    pipeline = Pipeline(
        model_name=args.model,
        params_name=args.params,
        data=df,
        freq=freq,
        pipeline_name=pipeline_name,
        base_dir_name=pathlib.Path(__file__).parent.absolute(),
    )

    # kwargs could contain:
    #             scalers,
    #             scaling_levels,
    #             weighted_loss,
    #             norm_types,
    #             norm_modes,
    #             norm_affines,
    # e.g. kwargs = {"scalers": [StandardScaler()], "scaling_levels": ["per_time_series"]}
    kwargs = {}

    start_time = time.time()
    pipeline.run(
        save=True,
        test_percentage=0.25,
        params_generator_name=args.gen_func,
        with_scalers=args.with_scalers,
        **kwargs
    )
    end_time = time.time()

    print("Pipeline execution time: ", end_time - start_time)
    pipeline.summary()
