import glob
import os
import pathlib
from shutil import copyfile

import pandas as pd


def merge_results():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    res_path = os.path.join(
        pathlib.Path(__file__).parent.parent.parent.absolute(), "results_no_scaler"
    )
    save_path = os.path.join(parent_dir, "tables")
    file_name_csv = os.path.join(save_path, "results_raw_no_scaler.csv")
    file_name_individual_csv = os.path.join(save_path, "results_indi_raw_no_scaler.csv")
    file_name_xlsx = os.path.join(save_path, "results_indi_raw_no_scaler.xlsx")

    # Make sure the directories exist
    os.makedirs(save_path, exist_ok=True)

    dfs_list = []
    dfs_list_individual = []

    for exp in os.listdir(res_path):
        exp_path = os.path.join(res_path, exp)
        if os.path.isdir(exp_path):
            results_csv_path = os.path.join(exp_path, "results.csv")
            print(results_csv_path)
            results_csv_pattern = glob.glob(os.path.join(exp_path, "results_*"))[0]
            print(results_csv_pattern)
            if os.path.isfile(results_csv_path):
                # read csv

                df = pd.read_csv(results_csv_path)
                df_individual = pd.read_csv(results_csv_pattern)

                # round the number to 4 decimal places
                df = df.round(4)
                df_individual = df_individual.round(4)

                # add ID column
                df["exp_id"] = exp
                df_individual["exp_id"] = exp
                # df['data_group_id'] = data_group
                df["scaling_level"] = df["scaling level"]
                df = df.drop("scaling level", axis=1)
                df = df.drop("data", axis=1)

                # append to the list
                dfs_list.append(df)
                dfs_list_individual.append(df_individual)

    # concatenate all dataframes
    df_merged = pd.concat(dfs_list, ignore_index=True).reset_index(drop=True)
    df_merged_individual = pd.concat(
        dfs_list_individual, ignore_index=True
    ).reset_index(drop=True)
    df_merged = df_merged.drop("Unnamed: 0", axis=1)
    # df_merged_2 = df_merged_2.drop('Unnamed: 0', axis=1)
    # replace nan in col norm_affine and norm_type with None
    df_merged["norm_affine"] = df_merged["norm_affine"].fillna("False")
    df_merged["norm_affine"] = df_merged["norm_affine"].replace("none", "False")
    df_merged["norm_affine"] = df_merged["norm_affine"].replace(False, "False")
    df_merged["norm_affine"] = df_merged["norm_affine"].replace(True, "True")
    df_merged["norm_type"] = df_merged["norm_type"].fillna("None")
    df_merged["norm_type"] = df_merged["norm_type"].replace("none", "None")
    df_merged["weighted"] = df_merged["weighted"].fillna("None")
    df_merged["weighted"] = df_merged["weighted"].replace("none", "None")
    df_merged["scaling_level"] = df_merged["scaling_level"].fillna("None")
    df_merged["scaling_level"] = df_merged["scaling_level"].replace("none", "None")
    df_merged["scaler"] = df_merged["scaler"].fillna("None")
    df_merged["scaler"] = df_merged["scaler"].replace("none", "None")
    df_merged["scaler"] = df_merged["scaler"].replace("no scaler", "None")
    # sort df
    df_merged = df_merged.sort_values(["exp_id"])
    df_merged_individual = df_merged_individual.sort_values(["exp_id", "ID"])

    # write to a csv file
    df_merged.to_excel(file_name_xlsx, index=False)
    df_merged.to_csv(file_name_csv, index=False)
    df_merged_individual.to_csv(file_name_individual_csv, index=False)
