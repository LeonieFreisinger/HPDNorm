import glob
import logging
import os
import pathlib

log = logging.getLogger("merging")

import pandas as pd
import numpy as np

from evaluation.helpers.params import (get_all_model_names,
                                       get_all_model_params,
                                       get_all_scaling_levels,
                                       get_default_scaler)


def parse_filename(filename):
    ALL_MODEL_NAMES = get_all_model_names()
    DEFAULT_SCALER = get_default_scaler()
    ALL_SCALING_LEVEL = get_all_scaling_levels()

    components = filename.split("_", 2)

    model = components[1]

    if len(components) == 2:
        # if there's no scaling level, assign None
        scaler = components[1]
        scaling_level = None
    else:
        remaining_string = components[2]
        # check each possible scaler to see if it's in the remaining_string
        for possible_scaler in DEFAULT_SCALER:
            if possible_scaler in remaining_string:
                scaler = possible_scaler
                # find the index where the scaler ends and use it to slice the remaining_string to get the scaling_level
                end_scaler_index = remaining_string.find(scaler) + len(scaler)
                scaling_level = (
                    remaining_string[end_scaler_index + 1 :]
                    if remaining_string[end_scaler_index + 1 :]
                    else None
                )
                break

    # Check if parsed components are valid
    if model not in ALL_MODEL_NAMES:
        raise ValueError(f"Unknown model name '{model}' in filename")
    if scaler not in DEFAULT_SCALER:
        raise ValueError(f"Unknown scaler '{scaler}' in filename")
    if scaling_level is not None and scaling_level not in ALL_SCALING_LEVEL:
        raise ValueError(f"Unknown scaling level '{scaling_level}' in filename")

    return model, scaler, scaling_level


def parse_folder_name(filename):
    ALL_MODEL_PARAMS = get_all_model_params()

    components = filename.split("_", 1)
    dataset = components[0]
    remaining_string = components[1]
    print(remaining_string)
    # check each possible scaler to see if it's in the remaining_string
    for param_name in ALL_MODEL_PARAMS:
        if param_name in remaining_string:
            model_id = param_name
            print("model_id", model_id)
            break

    # Check if parsed components are valid
    if param_name not in ALL_MODEL_PARAMS:
        raise ValueError(f"Unknown model param name '{param_name}' in filename")

    return dataset, model_id


def merge_results():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    res_path = os.path.join(
        pathlib.Path(__file__).parent.parent.parent.absolute(), "results_real_world"
    )
    save_path = os.path.join(parent_dir, "tables")
    file_name_csv = os.path.join(save_path, "results_indi_real_world.csv")
    # file_name_xlsx = os.path.join(save_path, "results_indi_raw_scaler.xlsx")

    # Make sure the directories exist
    os.makedirs(save_path, exist_ok=True)

    dfs_list = []

    for exp in os.listdir(res_path):
        exp_path = os.path.join(res_path, exp)
        if os.path.isdir(exp_path):
            print(exp_path)
            results_csv_files = glob.glob(os.path.join(exp_path, "results_*"))
            for results_csv_file in results_csv_files:
                print("Processing file:", results_csv_file)
                if os.path.isfile(results_csv_file):
                    # read csv
                    df = pd.read_csv(results_csv_file)

                    # round the number to 4 decimal places
                    df = df.round(4)

                    # add columns
                    df["exp_id"], df["model_id"] = parse_folder_name(exp)
                    # df['data_group_id'] = data_group
                    _, df["scaler"], df["scaling_level"] = parse_filename(
                        os.path.splitext(os.path.basename(results_csv_file))[0]
                    )

                    # append to the list
                    dfs_list.append(df)

    # concatenate all dataframes
    df_merged = pd.concat(dfs_list, ignore_index=True).reset_index(drop=True)
    df_merged["scaling_level"] = df_merged["scaling_level"].fillna("None")
    df_merged["scaling_level"] = df_merged["scaling_level"].replace("none", "None")
    df_merged = df_merged[~df_merged["scaling_level"].isin(["per_time_series_std"])]
    df_merged["scaling_level"] = df_merged["scaling_level"].replace(
        "per_time_series_none", "per_time_series"
    )
    df_merged["scaler"] = df_merged["scaler"].fillna("None")
    df_merged["scaler"] = df_merged["scaler"].replace("none", "None")
    df_merged["scaler"] = df_merged["scaler"].replace("no scaler", "None")
    df_merged["scaler"] = df_merged["scaler"].replace(
        "MinMaxScalerfeature_range=-0.5 0.5", "MinMaxScaler"
    )
    df_merged["scaler"] = df_merged["scaler"].replace(
        "RobustScalerquantile_range=5 95", "RobustScaler"
    )
    df_merged = df_merged[~(df_merged["scaler"] == "QuantileTransformeroutput_distribution='normal'")]

    # sort df
    df_merged = df_merged.sort_values(["exp_id", "ID"])

    # write to a csv file
    # df_merged.to_excel(file_name_xlsx, index=False)
    df_merged.to_csv(file_name_csv, index=False)

def parse_filename_wb(filename):
    parts = filename.split("_")
    norm_type = parts[2] if len(parts) > 2 else None
    norm_level = parts[3] if len(parts) > 3 else None
    learnable = parts[4] if len(parts) > 4 else None
    return norm_type, norm_level, learnable


def merge_results_wb():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    res_path = os.path.join(
        pathlib.Path(__file__).parent.parent.parent.absolute(), "results_real_world_window"
    )
    save_path = os.path.join(parent_dir, "tables")
    file_name_csv = os.path.join(save_path, "results_indi_real_world_window.csv")
    file_name_xlsx = os.path.join(save_path, "results_indi_real_world_window.xlsx")

    # Make sure the directories exist
    os.makedirs(save_path, exist_ok=True)

    dfs_list = []

    for exp in os.listdir(res_path):
        exp_path = os.path.join(res_path, exp)
        if os.path.isdir(exp_path):
            print(exp)
            if "NP_FNN_wb" in exp or "NP_FNN_wb_sw" in exp:
                results_csv_files = glob.glob(os.path.join(exp_path, "results_*"))
                for results_csv_file in results_csv_files:
                    print("Processing file:", results_csv_file)
                    if os.path.isfile(results_csv_file):
                        # read csv
                        df = pd.read_csv(results_csv_file)

                        # round the number to 4 decimal places
                        df = df.round(4)

                        # add columns
                        # add columns
                        df["exp_id"], df["model_id"] = parse_folder_name(exp)
                        filename = os.path.splitext(os.path.basename(results_csv_file))[
                            0
                        ]
                        (
                            df["norm_type"],
                            df["norm_level"],
                            df["learnable"],
                        ) = parse_filename_wb(filename)

                        # append to the list
                        dfs_list.append(df)
            elif "RNN_wb_in" in exp:
                results_csv_path = os.path.join(exp_path, "results_RNNModel_None.csv")
                if os.path.isfile(results_csv_path):
                    # read csv
                    df = pd.read_csv(results_csv_path)

                    # round the number to 4 decimal places
                    df = df.round(4)

                    # add columns
                    df["exp_id"], df["model_id"] = parse_folder_name(exp)
                    df["norm_type"] = "revin"
                    df["norm_level"] = "instance"
                    df["learnable"] = "None"

                    # append to the list
                    dfs_list.append(df)
            elif "RNN_wb_ba" in exp:
                results_csv_path = os.path.join(exp_path, "results_RNNModel_None.csv")
                if os.path.isfile(results_csv_path):
                    # read csv
                    df = pd.read_csv(results_csv_path)

                    # round the number to 4 decimal places
                    df = df.round(4)

                    # add columns
                    df["exp_id"], df["model_id"] = parse_folder_name(exp)
                    df["norm_type"] = "revin"
                    df["norm_level"] = "batch"
                    df["learnable"] = "None"

                    # append to the list
                    dfs_list.append(df)

    # concatenate all dataframes
    df_merged = pd.concat(dfs_list, ignore_index=True).reset_index(drop=True)
    print(df_merged)
    df_merged["learnable"] = df_merged["learnable"].fillna("None")
    df_merged["learnable"] = df_merged["learnable"].replace("none", "None")
    df_merged = df_merged[~df_merged["learnable"].isin(["affine"])]
    df_merged["norm_level"] = df_merged["norm_level"].fillna("None")
    df_merged["norm_level"] = df_merged["norm_level"].replace("none", "None")
    df_merged = df_merged[~df_merged["norm_type"].isin(["pytorch"])]
    df_merged = df_merged[~df_merged["norm_type"].isin(["None"])]
    # sort df
    df_merged = df_merged.sort_values(["exp_id", "ID"])

    # write to a csv file
    df_merged.to_excel(file_name_xlsx, index=False)
    df_merged.to_csv(file_name_csv, index=False)

def merge_both():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    results = pd.read_csv(
        os.path.join(tables_dir, "results_indi_real_world.csv"),
        index_col=["exp_id"],
    )
    results_window = pd.read_csv(
        os.path.join(tables_dir, "results_indi_real_world_window.csv"),
        index_col=["exp_id"],
    )
    file_name_csv = os.path.join(tables_dir, "results_indi_real_world_both.csv")

    all_cols = set(results.columns).union(
        set(results_window.columns)
    )

    # Reindex both dataframes to include all columns and fill NaN values with 'None'
    results = results.reindex(
        columns=all_cols, fill_value="None"
    )
    results_window = results_window.reindex(
        columns=all_cols, fill_value="None"
    )

    # Append df2 to df1
    appended_df = pd.concat([results, results_window], axis=0)

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


