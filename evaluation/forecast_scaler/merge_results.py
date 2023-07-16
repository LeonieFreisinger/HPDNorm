import glob
import logging
import os
import pathlib

log = logging.getLogger("merging")

import pandas as pd

from evaluation.helpers.params import (get_all_model_names,
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


def merge_results():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    res_path = os.path.join(
        pathlib.Path(__file__).parent.parent.parent.absolute(), "results_scaler"
    )
    save_path = os.path.join(parent_dir, "tables")
    file_name_csv = os.path.join(save_path, "results_indi_raw_scaler.csv")
    file_name_xlsx = os.path.join(save_path, "results_indi_raw_scaler.xlsx")

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
                    df["exp_id"] = exp
                    # df['data_group_id'] = data_group
                    _, df["scaler"], df["scaling_level"] = parse_filename(
                        os.path.splitext(os.path.basename(results_csv_file))[0]
                    )

                    # append to the list
                    dfs_list.append(df)

    # concatenate all dataframes
    df_merged = pd.concat(dfs_list, ignore_index=True).reset_index(drop=True)
    # df_merged = df_merged.drop("Unnamed: 0", axis=1)
    # df_merged_2 = df_merged_2.drop('Unnamed: 0', axis=1)
    # replace nan in col norm_affine and norm_type with None
    # df_merged["norm_affine"] = df_merged["norm_affine"].fillna("False")
    # df_merged["norm_affine"] = df_merged["norm_affine"].replace("none", "False")
    # df_merged["norm_affine"] = df_merged["norm_affine"].replace(False, "False")
    # df_merged["norm_affine"] = df_merged["norm_affine"].replace(True, "True")
    # df_merged["norm_type"] = df_merged["norm_type"].fillna("None")
    # df_merged["norm_type"] = df_merged["norm_type"].replace("none", "None")
    # df_merged["weighted"] = df_merged["weighted"].fillna("None")
    # df_merged["weighted"] = df_merged["weighted"].replace("none", "None")
    df_merged["scaling_level"] = df_merged["scaling_level"].fillna("None")
    df_merged["scaling_level"] = df_merged["scaling_level"].replace("none", "None")
    df_merged["scaler"] = df_merged["scaler"].fillna("None")
    df_merged["scaler"] = df_merged["scaler"].replace("none", "None")
    df_merged["scaler"] = df_merged["scaler"].replace("no scaler", "None")
    # sort df
    df_merged = df_merged.sort_values(["exp_id", "ID"])

    # write to a csv file
    df_merged.to_excel(file_name_xlsx, index=False)
    df_merged.to_csv(file_name_csv, index=False)
