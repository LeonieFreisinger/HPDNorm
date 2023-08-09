import os
import pathlib

import numpy as np
import pandas as pd

def calculate_all_statistics(
        metric, 
        base_error='MAE',
        selected_norm_level="default",
        selected_norm_type="default",                         
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_csv = os.path.join(tables_dir, f"statistics_{metric}_real_world_both_all.csv")
    df = pd.read_csv(
        os.path.join(tables_dir, f"{metric}_rel_to_no_real_world_both.csv"),
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
    max_val = df[base_error].max()
    min_val = df[base_error].min()
    summary_data.append([average, median, max_val, min_val])

    # Create a DataFrame for the summary data
    summary_df = pd.DataFrame(summary_data, columns=['average', 'median', 'max', 'min'])

    # Save the DataFrame to a CSV file
    summary_df.to_csv(file_name_csv, index=False)

def calculate_dataset_statistics(
        metric, 
        base_error='MAE',
        selected_norm_level="default",
        selected_norm_type="default",                         
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_csv = os.path.join(tables_dir, f"statistics_{metric}_real_world_both_per_dataset.csv")
    df = pd.read_csv(
        os.path.join(tables_dir, f"{metric}_rel_to_no_real_world_both.csv"),
    )
    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    # Initialize a list to store the medians for calculating the average
    medians = []
    averages = []
    max_values = []
    min_values = []

    # Initialize a list to store the dataset summary data
    summary_data = []

    unique_datasets = df["exp_id"].unique()

    # Calculate statistics for each dataset and write to the CSV file
    for dataset in unique_datasets:
        dataset_df = df[df["exp_id"] == dataset]
        median = dataset_df[base_error].median()
        average = dataset_df[base_error].mean()
        max_val = dataset_df[base_error].max()
        min_val = dataset_df[base_error].min()
        medians.append(median)
        averages.append(average)
        max_values.append(max_val)
        min_values.append(min_val)
        summary_data.append([dataset, median, average, max_val, min_val])

    # Calculate the average median
    average_median = sum(medians) / len(medians)
    average_average = (average).mean()
    overall_max = max(max_values)
    overall_min = min(min_values)

    # Create a DataFrame for the summary data
    summary_df = pd.DataFrame(summary_data, columns=['dataset', 'median', 'averga','max', 'min'])

    # Append the average median to the DataFrame
    summary_df = summary_df.append({'model': 'Average median', 'median': average_median, 'average': average_average, 'max': overall_max, 'min': overall_min}, ignore_index=True)

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
    file_name_csv = os.path.join(tables_dir, f"statistics_{metric}_real_world_both_per_model.csv")
    df = pd.read_csv(
        os.path.join(tables_dir, f"{metric}_rel_to_no_real_world_both.csv"),
    )
    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

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
