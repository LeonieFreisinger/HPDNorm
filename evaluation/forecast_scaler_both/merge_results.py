import os
import pathlib

import numpy as np
import pandas as pd


def merge_average_MASE():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    average_MASE_scaler = pd.read_csv(
        os.path.join(tables_dir, "average_MASE_scaler.csv"),
        index_col=["exp_id"],
    )
    average_MASE_scaler_window = pd.read_csv(
        os.path.join(tables_dir, "average_MASE_scaler_window.csv"),
        index_col=["exp_id"],
    )
    file_name_csv = os.path.join(tables_dir, "average_MASE_scaler_both.csv")

    all_cols = set(average_MASE_scaler.columns).union(
        set(average_MASE_scaler_window.columns)
    )

    # Reindex both dataframes to include all columns and fill NaN values with 'None'
    average_MASE_scaler = average_MASE_scaler.reindex(
        columns=all_cols, fill_value="None"
    )
    average_MASE_scaler_window = average_MASE_scaler_window.reindex(
        columns=all_cols, fill_value="None"
    )

    # Append df2 to df1
    appended_df = pd.concat([average_MASE_scaler, average_MASE_scaler_window], axis=0)

    # Create the new 'type' and 'level' columns
    appended_df["type"] = np.where(
        appended_df["norm_type"] != "None",
        appended_df["norm_type"],
        appended_df["scaler"],
    )
    appended_df["level"] = np.where(
        appended_df["norm_level"] != "None",
        appended_df["norm_level"],
        appended_df["scaling_level"],
    )

    # Drop the five original columns
    appended_df = appended_df.drop(
        columns=["norm_type", "norm_level", "learnable", "scaler", "scaling_level"]
    )

    appended_df.to_csv(file_name_csv)


def merge_scaled_agg_MAE():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    scaled_agg_MAE = pd.read_csv(
        os.path.join(tables_dir, "scaled_agg_MAE_scaler.csv"),
        index_col=["exp_id"],
    )
    scaled_agg_MAE_window = pd.read_csv(
        os.path.join(tables_dir, "scaled_agg_MAE_scaler_window.csv"),
        index_col=["exp_id"],
    )
    file_name_csv = os.path.join(tables_dir, "scaled_agg_MAE_scaler_both.csv")

    all_cols = set(scaled_agg_MAE.columns).union(set(scaled_agg_MAE_window.columns))

    # Reindex both dataframes to include all columns and fill NaN values with 'None'
    scaled_agg_MAE = scaled_agg_MAE.reindex(columns=all_cols, fill_value="None")
    scaled_agg_MAE_window = scaled_agg_MAE_window.reindex(
        columns=all_cols, fill_value="None"
    )

    # Append df2 to df1
    appended_df = pd.concat([scaled_agg_MAE, scaled_agg_MAE_window], axis=0)
    # print(appended_df)
    # appended_df = appended_df.drop(columns=['Unnamed: 0'])
    # Create the new 'type' and 'level' columns
    appended_df["type"] = np.where(
        appended_df["norm_type"] != "None",
        appended_df["norm_type"],
        appended_df["scaler"],
    )
    appended_df["level"] = np.where(
        appended_df["norm_level"] != "None",
        appended_df["norm_level"],
        appended_df["scaling_level"],
    )

    # Drop the five original columns
    appended_df = appended_df.drop(
        columns=["norm_type", "norm_level", "learnable", "scaler", "scaling_level"]
    )

    appended_df.to_csv(file_name_csv)
