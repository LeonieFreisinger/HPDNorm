import os
import pathlib

import pandas as pd
import plotly.express as px
import plotly.io as pio

from evaluation.helpers.params import get_het_type_order, get_model_id_order


def parse_exp_id(df):
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
    df_exp = df_exp.drop(columns=["exp_id"])
    return df_exp


def view_best_scaler_dif_to_no_scaler_for_metric_per_model_and_het_type(
    metric, columns_to_show
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    if "norm_type" in columns_to_show:
        file_name_csv = os.path.join(
            tables_dir, f"view_best_scaler_type_dif_to_no_scaler_{metric}_window.csv"
        )
    else:
        file_name_csv = os.path.join(
            tables_dir, f"view_best_scaler_dif_to_no_scaler_{metric}_window.csv"
        )

    if metric in ["average_MASE", "scaled_agg_MAE"]:
        metric_df = pd.read_csv(
            os.path.join(
                tables_dir, f"best_scaler_dif_to_no_scaler_{metric}_window.csv"
            ),
        )
    else:
        raise ValueError(f"Invalid metric {metric}")

    metric_df = parse_exp_id(metric_df)
    metric_df["het_strength"] = metric_df["het_strength"].astype(float)
    metric_df = metric_df[~metric_df["model_id"].isin(["Naive", "SNaive"])]

    # Ensure that columns_to_show is a list
    if isinstance(columns_to_show, str):
        columns_to_show = [columns_to_show]

    # Check if specified columns exist in the dataframe
    for column in columns_to_show:
        if column not in metric_df.columns:
            raise ValueError(f"Column {column} does not exist in the DataFrame.")

    df_metric_pivot = metric_df.pivot_table(
        index="model_id", columns="het_type", values=columns_to_show, aggfunc="first"
    )
    df_metric_pivot = df_metric_pivot.swaplevel(0, 1, axis=1).sort_index(axis=1)
    # Define order
    model_id_order = [
        "NP_FNN",
        "NP_FNN_sw",
        "RNN",
    ]  # replace with your actual desired order
    het_type_order = get_het_type_order()  # replace with your actual desired order

    # Reorder index and columns
    df_metric_pivot = df_metric_pivot.loc[model_id_order, het_type_order]
    # Write to a csv file
    df_metric_pivot.to_csv(file_name_csv)


def plot_bar_plots_best_scaler_dif_to_no(
    metric, metric_to_plot
):  # Again, we assume df_metric_pivot has been reset so multi-index is now columns
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(
        figures_dir, f"barplot_best_scaler_dif_to_no_scaler_{metric}_window.png"
    )
    model_id_order = ["NP_FNN", "NP_FNN_sw", "RNN"]
    het_type_order = get_het_type_order()

    if metric in ["average_MASE", "scaled_agg_MAE"]:
        metric_df = pd.read_csv(
            os.path.join(
                tables_dir, f"best_scaler_dif_to_no_scaler_{metric}_window.csv"
            ),
        )
    else:
        raise ValueError(f"Invalid metric {metric}")

    metric_df = parse_exp_id(metric_df)
    metric_df = metric_df.drop("het_strength", axis=1)
    metric_df = metric_df[~metric_df["model_id"].isin(["Naive", "SNaive"])]
    # print(metric_df)

    # create a grouped bar plot
    fig = px.bar(
        metric_df,
        x="model_id",
        y=metric_to_plot,
        color="het_type",
        barmode="group",
        title="MAE by model and het_type",
        category_orders={"model_id": model_id_order, "het_type": het_type_order},
        width=1400,
        height=600,
    )
    pio.write_image(fig, file_name_png)
