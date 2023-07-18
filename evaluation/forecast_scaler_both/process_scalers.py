import os
import pathlib

import pandas as pd


def calculate_best_scalers_both(metric):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    if metric == "average_MASE":
        best_scaler = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_average_MASE.csv"),
            index_col=["exp_id"],
        )
        best_scaler_window = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_average_MASE_window.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(tables_dir, "best_scaler_average_MASE_both.csv")
    if metric == "scaled_agg_MAE":
        best_scaler = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_scaled_agg_MAE.csv"),
            index_col=["exp_id"],
        )
        best_scaler_window = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_scaled_agg_MAE_window.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(tables_dir, "best_scaler_scaled_agg_MAE_both.csv")
    # Add 'normalization' column to each dataframe
    best_scaler["normalization"] = "full-series"
    best_scaler_window["normalization"] = "window-based"
    # Merge the two dataframes on 'exp_id'
    # Find all columns
    all_cols = set(best_scaler.columns).union(set(best_scaler_window.columns))

    # Reindex both dataframes to include all columns and fill NaN values with 'None'
    best_scaler = best_scaler.reindex(columns=all_cols, fill_value="None")
    best_scaler_window = best_scaler_window.reindex(columns=all_cols, fill_value="None")

    # Append df2 to df1
    appended_df = pd.concat([best_scaler, best_scaler_window], axis=0)

    appended_df = appended_df.drop(columns=["Unnamed: 0"])
    appended_df.to_csv(file_name_csv)


def calculate_best_scalers_combined(metric):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    if metric == "average_MASE":
        best_scaler_both = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_average_MASE_both.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_average_MASE_combined.csv"
        )
    if metric == "scaled_agg_MAE":
        best_scaler_both = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_scaled_agg_MAE_both.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_scaled_agg_MAE_combined.csv"
        )
    # Convert 'MAE' to numeric type for proper comparison
    best_scaler_both["MAE"] = pd.to_numeric(best_scaler_both["MAE"], errors="coerce")

    # Sort by 'MAE'
    best_scaler_both.sort_values("MAE", inplace=True)

    # Drop duplicates by 'exp_id' and keep the first one (i.e., the one with smaller 'MAE')
    best_scaler_both = best_scaler_both.reset_index()
    best_scaler_both.drop_duplicates(subset="exp_id", keep="first", inplace=True)
    best_scaler_both.set_index("exp_id", inplace=True)
    # Reset index
    best_scaler_both.to_csv(file_name_csv)


def calculate_best_scaler_rel_to_no_scaler_for_metric(metric, mode):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    if metric == "average_MASE" and mode == "both":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_average_MASE_both.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "average_MASE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_rel_to_no_scaler_average_MASE_both.csv"
        )
    if metric == "scaled_agg_MAE" and mode == "both":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_scaled_agg_MAE_both.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "scaled_agg_MAE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_rel_to_no_scaler_scaled_agg_MAE_both.csv"
        )
    if metric == "average_MASE" and mode == "combined":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_average_MASE_combined.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "average_MASE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_rel_to_no_scaler_average_MASE_combined.csv"
        )
    if metric == "scaled_agg_MAE" and mode == "combined":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_scaled_agg_MAE_combined.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "scaled_agg_MAE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_rel_to_no_scaler_scaled_agg_MAE_combined.csv"
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
    metric_df_rel_to_no_scaler[
        ["scaler", "scaling_level", "norm_type", "norm_level", "learnable"]
    ] = metric_df[["scaler", "scaling_level", "norm_type", "norm_level", "learnable"]]
    # Write to a csv file
    metric_df_rel_to_no_scaler.to_csv(file_name_csv)

    def calculate_best_scalers_combined(metric):
        parent_dir = pathlib.Path(__file__).parent.parent.absolute()
        tables_dir = os.path.join(parent_dir, "tables")
        if metric == "average_MASE":
            best_scaler_both = pd.read_csv(
                os.path.join(tables_dir, "best_scaler_average_MASE_both.csv"),
                index_col=["exp_id"],
            )
            file_name_csv = os.path.join(
                tables_dir, "best_scaler_average_MASE_combined.csv"
            )
        if metric == "scaled_agg_MAE":
            best_scaler_both = pd.read_csv(
                os.path.join(tables_dir, "best_scaler_scaled_agg_MAE_both.csv"),
                index_col=["exp_id"],
            )
            file_name_csv = os.path.join(
                tables_dir, "best_scaler_scaled_agg_MAE_combined.csv"
            )
        # Convert 'MAE' to numeric type for proper comparison
        best_scaler_both["MAE"] = pd.to_numeric(
            best_scaler_both["MAE"], errors="coerce"
        )

        # Sort by 'MAE'
        best_scaler_both.sort_values("MAE", inplace=True)

        # Drop duplicates by 'exp_id' and keep the first one (i.e., the one with smaller 'MAE')
        best_scaler_both = best_scaler_both.reset_index()
        best_scaler_both.drop_duplicates(subset="exp_id", keep="first", inplace=True)
        best_scaler_both.set_index("exp_id", inplace=True)
        # Reset index
        best_scaler_both.to_csv(file_name_csv)


def calculate_best_scaler_rel_to_no_scaler_for_metric(metric, mode):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    if metric == "average_MASE" and mode == "both":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_average_MASE_both.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "average_MASE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_rel_to_no_scaler_average_MASE_both.csv"
        )
    if metric == "scaled_agg_MAE" and mode == "both":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_scaled_agg_MAE_both.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "scaled_agg_MAE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_rel_to_no_scaler_scaled_agg_MAE_both.csv"
        )
    if metric == "average_MASE" and mode == "combined":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_average_MASE_combined.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "average_MASE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_rel_to_no_scaler_average_MASE_combined.csv"
        )
    if metric == "scaled_agg_MAE" and mode == "combined":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "best_scaler_scaled_agg_MAE_combined.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "scaled_agg_MAE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "best_scaler_rel_to_no_scaler_scaled_agg_MAE_combined.csv"
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
    metric_df_rel_to_no_scaler[
        ["scaler", "scaling_level", "norm_type", "norm_level", "learnable"]
    ] = metric_df[["scaler", "scaling_level", "norm_type", "norm_level", "learnable"]]
    # Write to a csv file
    metric_df_rel_to_no_scaler.to_csv(file_name_csv)


def calculate_all_rel_to_no_scaler_for_metric(metric):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    temp1 = os.path.join(tables_dir, "temp1.csv")
    temp2 = os.path.join(tables_dir, "temp2.csv")
    temp3 = os.path.join(tables_dir, "temp3.csv")

    if metric == "average_MASE":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "average_MASE_scaler_both.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "average_MASE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "average_MASE_rel_to_no_scaler_both.csv"
        )
    if metric == "scaled_agg_MAE":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "scaled_agg_MAE_scaler_both.csv"),
            index_col=["exp_id"],
        )
        metric_df_no_scaler = pd.read_csv(
            os.path.join(tables_dir, "scaled_agg_MAE_no_scaler.csv"),
            index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "scaled_agg_MAE_rel_to_no_scaler_both.csv"
        )

    idx = metric_df.index

    # Filter rows in ideal_metrics_sampled where the multi-index matches
    filtered_metric_df_no_scaler = metric_df_no_scaler[
        metric_df_no_scaler.index.isin(idx)
    ]
    metric_df = metric_df.sort_index()
    filtered_metric_df_no_scaler = filtered_metric_df_no_scaler.sort_index()

    metric_df_rel_to_no_scaler = (
        filtered_metric_df_no_scaler[["MAE", "RMSE"]]
        .subtract(metric_df[["MAE", "RMSE"]])
        .div(filtered_metric_df_no_scaler[["MAE", "RMSE"]])
    )

    metric_df_rel_to_no_scaler = metric_df_rel_to_no_scaler.reset_index()
    metric_df = metric_df.reset_index()
    print(metric_df_rel_to_no_scaler)
    metric_df_rel_to_no_scaler[["type", "level"]] = metric_df[["type", "level"]]
    metric_df_rel_to_no_scaler.set_index("exp_id", inplace=True)
    # Write to a csv file
    metric_df_rel_to_no_scaler.to_csv(file_name_csv)
