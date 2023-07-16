import glob
import os
import pathlib

import pandas as pd


def parse_filename(filename):
    parts = filename.split("_")
    norm_type = parts[2] if len(parts) > 2 else None
    norm_level = parts[3] if len(parts) > 3 else None
    learnable = parts[4] if len(parts) > 4 else None
    return norm_type, norm_level, learnable


def merge_results():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    res_path = os.path.join(
        pathlib.Path(__file__).parent.parent.parent.absolute(), "results_window"
    )
    save_path = os.path.join(parent_dir, "tables")
    file_name_csv = os.path.join(save_path, "results_indi_raw_scaler_window.csv")
    file_name_xlsx = os.path.join(save_path, "results_indi_raw_scaler_window.xlsx")

    # Make sure the directories exist
    os.makedirs(save_path, exist_ok=True)

    dfs_list = []

    for exp in os.listdir(res_path):
        exp_path = os.path.join(res_path, exp)
        if os.path.isdir(exp_path):
            print(exp)
            if exp.startswith("NP_FNN"):
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
                        filename = os.path.splitext(os.path.basename(results_csv_file))[
                            0
                        ]
                        (
                            df["norm_type"],
                            df["norm_level"],
                            df["learnable"],
                        ) = parse_filename(filename)

                        # append to the list
                        dfs_list.append(df)
            elif exp.startswith("RNN_wb_in"):
                results_csv_path = os.path.join(exp_path, "results_RNNModel_None.csv")
                if os.path.isfile(results_csv_path):
                    # read csv
                    df = pd.read_csv(results_csv_path)

                    # round the number to 4 decimal places
                    df = df.round(4)

                    # add columns
                    df["exp_id"] = exp
                    df["norm_type"] = "revin"
                    df["norm_level"] = "instance"
                    df["learnable"] = "None"

                    # append to the list
                    dfs_list.append(df)
            elif exp.startswith("RNN_wb_ba"):
                results_csv_path = os.path.join(exp_path, "results_RNNModel_None.csv")
                if os.path.isfile(results_csv_path):
                    # read csv
                    df = pd.read_csv(results_csv_path)

                    # round the number to 4 decimal places
                    df = df.round(4)

                    # add columns
                    df["exp_id"] = exp
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
    df_merged["norm_level"] = df_merged["norm_level"].fillna("None")
    df_merged["norm_level"] = df_merged["norm_level"].replace("none", "None")
    # sort df
    df_merged = df_merged.sort_values(["exp_id", "ID"])

    # write to a csv file
    df_merged.to_excel(file_name_xlsx, index=False)
    df_merged.to_csv(file_name_csv, index=False)
