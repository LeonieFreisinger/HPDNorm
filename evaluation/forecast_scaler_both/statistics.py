import os
import pathlib

import numpy as np
import pandas as pd

def parse_exp_id(df, inplace=False):
    df_exp = df.copy()
    # Replace structural_break with structuralBreak so it won't be split
    df_exp["exp_id"] = df_exp["exp_id"].str.replace(
        "structural_break", "structuralBreak"
    )
    # Note the change in the rsplit function arguments
    df_exp[["model_id", "het_type", "het_strength"]] = df_exp["exp_id"].str.rsplit(
        pat="_", n=2, expand=True
    )
    # Change structuralBreak back to structural_break
    df_exp["het_type"] = df_exp["het_type"].replace(
        "structuralBreak", "structural_break"
    )
    if inplace is False:
        df_exp = df_exp.drop(columns=["exp_id"])
    return df_exp

def calculate_all_statistics(
        metric, 
        base_error='MAE',
        selected_norm_level="default",
        selected_norm_type="default",                         
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_csv = os.path.join(tables_dir, f"statistics_{metric}_all.csv")
    df = pd.read_csv(
        os.path.join(tables_dir, f"{metric}_rel_to_no_scaler_both.csv"),
    )
    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    # Initialize a list to store the dataset summary data
    summary_data = []

    # Calculate statistics for each dataset and write to the CSV file
    average = df[base_error].mean()
    median = df[base_error].median()
    q1 = df[base_error].quantile(0.25)
    q3 = df[base_error].quantile(0.75)
    max_val = df[base_error].max()
    min_val = df[base_error].min()
    summary_data.append([average, median, max_val, min_val, q3, q1])

    # Create a DataFrame for the summary data
    summary_df = pd.DataFrame(summary_data, columns=['avergae','median', 'max', 'min', 'q3', 'q1'])

    # Save the DataFrame to a CSV file
    summary_df.to_csv(file_name_csv, index=False)

def calculate_het_type_statistics(
        metric, 
        base_error='MAE',
        selected_norm_level="default",
        selected_norm_type="default",                         
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_csv = os.path.join(tables_dir, f"statistics_{metric}_per_het_type.csv")
    df = pd.read_csv(
        os.path.join(tables_dir, f"{metric}_rel_to_no_scaler_both.csv"),
    )
    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    df = parse_exp_id(df)

    # Initialize a list to store the medians for calculating the average
    medians = []
    max_values = []
    min_values = []

    # Initialize a list to store the dataset summary data
    summary_data = []

    unique_het_types = df["het_type"].unique()

    # Calculate statistics for each dataset and write to the CSV file
    for het_type in unique_het_types:
        het_type_df = df[df["het_type"] == het_type]
        median = het_type_df[base_error].median()
        max_val = het_type_df[base_error].max()
        min_val = het_type_df[base_error].min()
        medians.append(median)
        max_values.append(max_val)
        min_values.append(min_val)
        summary_data.append([het_type, median, max_val, min_val])

    # Calculate the average median
    average_median = sum(medians) / len(medians)
    overall_max = max(max_values)
    overall_min = min(min_values)

    # Create a DataFrame for the summary data
    summary_df = pd.DataFrame(summary_data, columns=['het_type', 'median', 'max', 'min'])

    # Append the average median to the DataFrame
    summary_df = summary_df.append({'model': 'Average median', 'median': average_median, 'max': overall_max, 'min': overall_min}, ignore_index=True)

    # Save the DataFrame to a CSV file
    summary_df.to_csv(file_name_csv, index=False)


def calculate_model_statistics(
        metric, 
        base_error='MAE',
        selected_norm_level="default",
        selected_norm_type="default",                         
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_csv = os.path.join(tables_dir, f"statistics_{metric}_per_model.csv")
    df = pd.read_csv(
        os.path.join(tables_dir, f"{metric}_rel_to_no_scaler_both.csv"),
    )
    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    df = parse_exp_id(df)

    # Initialize a list to store the medians for calculating the average
    medians = []
    max_values = []
    min_values = []

    # Initialize a list to store the dataset summary data
    summary_data = []

    unique_models = df["model_id"].unique()

    # Calculate statistics for each dataset and write to the CSV file
    for model in unique_models:
        dataset_df = df[df["model_id"] == model]
        median = dataset_df[base_error].median()
        max_val = dataset_df[base_error].max()
        min_val = dataset_df[base_error].min()
        medians.append(median)
        max_values.append(max_val)
        min_values.append(min_val)
        summary_data.append([model, median, max_val, min_val])

    # Calculate the average median
    average_median = sum(medians) / len(medians)
    overall_max = max(max_values)
    overall_min = min(min_values)

    # Create a DataFrame for the summary data
    summary_df = pd.DataFrame(summary_data, columns=['model', 'median', 'max', 'min'])

    # Append the average median to the DataFrame
    summary_df = summary_df.append({'model': 'Average median', 'median': average_median, 'max': overall_max, 'min': overall_min}, ignore_index=True)

    # Save the DataFrame to a CSV file
    summary_df.to_csv(file_name_csv, index=False)
