import os
import pathlib

import pandas as pd


def postprocess_results_indi_df(original_df):
    df = original_df.copy()
    df = df[df["ID"] != "ALL"]
    # df.loc[:, "ID"] = df["ID"].astype(int)
    df_filtered = df[
        ["exp_id", "ID", "MAE", "RMSE", "scaler", "scaling_level", "model_id"]
    ]
    return df_filtered


def calculate_average_MASE():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    results_indi_merged = pd.read_csv(
        os.path.join(tables_dir, "results_indi_real_world.csv")
    )
    file_name_csv = os.path.join(tables_dir, "average_MASE_real_world.csv")
    df_error = results_indi_merged[
        ~results_indi_merged["model_id"].isin(["Naive", "SNaive"])
    ]
    df_ideal_error = results_indi_merged[results_indi_merged["model_id"] == "Naive"]

    # Reset the index
    idx = pd.MultiIndex.from_frame(
        df_ideal_error[["ID", "exp_id", "scaler", "scaling_level"]]
    )

    # Filter rows in ideal_metrics_sampled where the multi-index matches
    filtered_df_ideal_error = df_ideal_error  # [df_ideal_error.index.isin(idx)]
    print(filtered_df_ideal_error)
    df_error = postprocess_results_indi_df(df_error)
    filtered_df_ideal_error = postprocess_results_indi_df(filtered_df_ideal_error)

    filtered_df_ideal_error[
        ["ID", "exp_id", "scaler", "scaling_level"]
    ] = filtered_df_ideal_error[["ID", "exp_id", "scaler", "scaling_level"]].astype(str)
    filtered_df_ideal_error.set_index(
        ["ID", "exp_id", "scaler", "scaling_level"], inplace=True
    )

    df_error[["ID", "exp_id", "scaler", "scaling_level"]] = df_error[
        ["ID", "exp_id", "scaler", "scaling_level"]
    ].astype(str)
    df_error.set_index(["ID", "exp_id", "scaler", "scaling_level"], inplace=True)

    filtered_df_ideal_error.sort_index()
    df_error.sort_index()

    # Create a new DataFrame for division operation
    div_result = (
        df_error[["MAE", "RMSE"]]
        .div(filtered_df_ideal_error[["MAE", "RMSE"]])
        .reset_index()
    )

    df_error.reset_index(inplace=True)
    print(filtered_df_ideal_error)
    print(div_result)
    # Concat other columns from df_error
    average_MASE_per_ID = pd.concat([div_result, df_error[["model_id"]]], axis=1)
    average_MASE = average_MASE_per_ID
    # average_MASE = average_MASE_per_ID.groupby(
    #     ["exp_id","model_id", "scaler", "scaling_level"]
    # ).mean()
    average_MASE.to_csv(file_name_csv)


def calculate_scaled_agg_MAE():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    results_indi_merged = pd.read_csv(
        os.path.join(tables_dir, "results_indi_raw_scaler.csv")
    )
    ideal_metrics_sampled = pd.read_csv(
        os.path.join(tables_dir, "df_ideal_metrics_sampled.csv"),
        index_col=[0, 1],
        header=[0],
    )
    file_name_csv = os.path.join(tables_dir, "scaled_agg_MAE_scaler.csv")

    # Converting the second level of the index to str and sorting the index
    ideal_metrics_sampled.index = ideal_metrics_sampled.index.set_levels(
        ideal_metrics_sampled.index.levels[0], level=0
    ).set_levels(ideal_metrics_sampled.index.levels[1].astype(str), level=1)
    ideal_metrics_sampled.sort_index(inplace=True)

    idx = pd.MultiIndex.from_frame(results_indi_merged[["exp_id", "ID"]])

    # Filter rows in ideal_metrics_sampled where the multi-index matches
    filtered_ideal_metrics_sampled = ideal_metrics_sampled[
        ideal_metrics_sampled.index.isin(idx)
    ]

    df_error = postprocess_results_indi_df(results_indi_merged).sort_index()
    # Check if indices are the same

    df_error.index = pd.MultiIndex.from_tuples(
        [tuple(map(str, i)) for i in df_error.index.to_list()],
        names=df_error.index.names,
    )
    filtered_ideal_metrics_sampled.index = pd.MultiIndex.from_tuples(
        [tuple(map(str, i)) for i in filtered_ideal_metrics_sampled.index.to_list()],
        names=filtered_ideal_metrics_sampled.index.names,
    )

    # create both averaged error
    df_error_averaged_over_ID = df_error.groupby(
        ["exp_id", "scaler", "scaling_level"]
    ).mean()
    print(df_error_averaged_over_ID)
    df_ideal_error_averaged_over_ID = filtered_ideal_metrics_sampled.groupby(
        ["exp_id"]
    ).mean()

    # Create a new DataFrame for division operation
    scaled_agg_MAE = df_error_averaged_over_ID[["MAE", "RMSE"]].div(
        df_ideal_error_averaged_over_ID[["MAE", "RMSE"]]
    )
    scaled_agg_MAE.to_csv(file_name_csv)


def calculate_best_scaler_for_metric(metric):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    if metric == "average_MASE":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "average_MASE_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(tables_dir, "best_scaler_average_MASE.csv")
    if metric == "scaled_agg_MAE":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "scaled_agg_MAE_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(tables_dir, "best_scaler_scaled_agg_MAE.csv")

    # Filter out unwanted scaler
    metric_df = metric_df[
        metric_df["scaler"] != "QuantileTransformeroutput_distribution='normal'"
    ]

    # Reset the index
    metric_df_reset = metric_df.reset_index()

    # Group by 'exp_id' and find the index of the minimum 'MAE'
    best_combinations_idx = metric_df_reset.groupby("exp_id")["MAE"].idxmin()

    # Use the indices to get the rows with the best combinations
    best_combinations_df = metric_df_reset.loc[best_combinations_idx]

    # Write to a csv file
    best_combinations_df.to_csv(file_name_csv)


def calculate_best_scaler_rel_to_no_scaler_for_metric(metric):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    if metric == "average_MASE":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_average_MASE.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "average_MASE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_rel_to_no_scaler_average_MASE.csv"
        )
    if metric == "scaled_agg_MAE":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_scaled_agg_MAE.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "scaled_agg_MAE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_rel_to_no_scaler_scaled_agg_MAE.csv"
        )

    idx = metric_df.index

    # Filter rows in ideal_metrics_sampled where the multi-index matches
    filtered_metric_df_no_scaler = metric_df_no_scaler[
        metric_df_no_scaler.index.isin(idx)
    ]
    metric_df_rel_to_no_scaler = (
        filtered_metric_df_no_scaler[["MAE", "RMSE"]]
        .subtract(metric_df[["MAE", "RMSE"]])
        .div(filtered_metric_df_no_scaler[["MAE", "RMSE"]])
    )
    metric_df_rel_to_no_scaler[["scaler", "scaling_level"]] = metric_df[
        ["scaler", "scaling_level"]
    ]
    # Write to a csv file
    metric_df_rel_to_no_scaler.to_csv(file_name_csv)
