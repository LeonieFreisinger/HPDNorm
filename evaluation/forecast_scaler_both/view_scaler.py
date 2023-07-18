import os
import pathlib

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from evaluation.helpers.layout import create_layout

layout, het_type_colors, model_id_colors = create_layout()


from evaluation.helpers.params import (get_full_het_names,
                                       get_full_model_names,
                                       get_het_type_order, get_model_id_order)


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


def view_best_scaler_rel_to_no_scaler_for_metric_per_model_and_het_type(metric):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")

    file_name_csv = os.path.join(
        tables_dir, f"view_best_scaler_type_rel_to_no_scaler_{metric}_combined.csv"
    )

    if metric in ["average_MASE", "scaled_agg_MAE"]:
        metric_df = pd.read_csv(
            os.path.join(
                tables_dir, f"best_scaler_rel_to_no_scaler_{metric}_combined.csv"
            ),
        )
    else:
        raise ValueError(f"Invalid metric {metric}")
    metric_df = parse_exp_id(metric_df)

    # Create the new 'type' and 'level' columns
    metric_df["type"] = np.where(
        metric_df["norm_type"] != "None", metric_df["norm_type"], metric_df["scaler"]
    )
    metric_df["level"] = np.where(
        metric_df["norm_level"] != "None",
        metric_df["norm_level"],
        metric_df["scaling_level"],
    )

    # Drop the five original columns
    metric_df = metric_df.drop(
        columns=["norm_type", "norm_level", "learnable", "scaler", "scaling_level"]
    )

    metric_df["het_strength"] = metric_df["het_strength"].astype(float)
    metric_df = metric_df[~metric_df["model_id"].isin(["Naive", "SNaive"])]
    print(metric_df)

    df_metric_pivot = metric_df.pivot_table(
        index="model_id", columns="het_type", values=["type", "level"], aggfunc="first"
    )
    df_metric_pivot = df_metric_pivot.swaplevel(0, 1, axis=1).sort_index(axis=1)
    # Define order
    model_id_order = get_model_id_order()
    het_type_order = get_het_type_order()  # replace with your actual desired order

    # Reorder index and columns
    df_metric_pivot = df_metric_pivot.loc[model_id_order, het_type_order]
    # Write to a csv file
    df_metric_pivot.to_csv(file_name_csv)


def plot_bar_plots_best_scaler_rel_to_no(
    metric, metric_to_plot
):  # Again, we assume df_metric_pivot has been reset so multi-index is now columns
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png_overview = os.path.join(
        figures_dir, f"barplot_best_scaler_rel_to_no_scaler_{metric}_combined.png"
    )
    file_name_png_avg_per_model = os.path.join(
        figures_dir,
        f"barplot_best_scaler_rel_to_no_scaler_avgpmodel_{metric}_combined.png",
    )
    file_name_png_avg_per_het_type = os.path.join(
        figures_dir,
        f"barplot_best_scaler_rel_to_no_scaler_avgphettype_{metric}_combined.png",
    )
    model_id_order = get_model_id_order()
    het_type_order = get_het_type_order()

    if metric in ["average_MASE", "scaled_agg_MAE"]:
        metric_df = pd.read_csv(
            os.path.join(
                tables_dir, f"best_scaler_rel_to_no_scaler_{metric}_combined.csv"
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
    pio.write_image(fig, file_name_png_overview)

    # Average over all het_types for each model
    avg_model_df = metric_df.groupby("model_id").mean().reset_index()

    # Create the second bar plot
    fig2 = px.bar(
        avg_model_df,
        x="model_id",
        y=metric_to_plot,
        title="Average MAE by model",
        category_orders={"model_id": model_id_order},
        width=1400,
        height=600,
    )
    pio.write_image(fig2, file_name_png_avg_per_model)

    # Average over all model_ids for each het_type
    avg_het_type_df = metric_df.groupby("het_type").mean().reset_index()

    # Create the third bar plot
    fig3 = px.bar(
        avg_het_type_df,
        x="het_type",
        y=metric_to_plot,
        title="Average MAE by heterogeneity type",
        category_orders={"het_type": het_type_order},
        width=1400,
        height=600,
    )
    pio.write_image(fig3, file_name_png_avg_per_het_type)


def create_faceted_box_plots(
    metric,
    base_error="MAE",
    selected_norm_level="default",
    selected_norm_type="default",
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(figures_dir, f"box_plots_all_{metric}_both.png")
    df = pd.read_csv(
        os.path.join(tables_dir, f"{metric}_rel_to_no_scaler_both.csv"),
    )

    # Generate relevant cols model_id, het_type, het_strength
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    df = parse_exp_id(df, inplace=True)
    remove_ids = ["Naive", "SNaive"]
    df = df[~df["model_id"].isin(remove_ids)]

    # remove normalization type and level, that has not been selected
    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    print(df)
    # Get unique exp_ids
    unique_het_types = df["het_type"].unique()
    unique_model_ids = df["model_id"].unique()

    model_id_order = get_model_id_order()
    het_type_order = get_het_type_order()
    full_model_names = get_full_model_names()
    full_het_names = get_full_het_names()

    # Sort unique_model_ids and unique_het_types according to their respective orders
    unique_model_ids = sorted(unique_model_ids, key=lambda x: model_id_order.index(x))
    unique_het_types = sorted(unique_het_types, key=lambda x: het_type_order.index(x))

    # Specify different colors for different het_types
    colors = {
        het_type: het_type_colors[i] for i, het_type in enumerate(unique_het_types)
    }

    # Create subplots, with one column for each model_id
    fig = (
        go.Figure()
    )  # make_subplots(rows=1, cols=len(unique_model_ids), subplot_titles=unique_model_ids)

    offset = np.linspace(-0.3, 0.3, len(unique_het_types))
    # Initialize an empty set to keep track of legend items
    legend_items = set()

    for i, model_id in enumerate(unique_model_ids):
        for j, het_type in enumerate(unique_het_types):
            # Filter dataframe for each het_type and model_id
            het_type_df = df[
                (df["model_id"] == model_id) & (df["het_type"] == het_type)
            ]

            # Add a boxplot for each het_type for the specific model_id
            fig.add_trace(
                go.Box(
                    y=het_type_df[base_error],
                    name=full_het_names.get(het_type, het_type),
                    legendgroup=het_type,
                    boxpoints="all",
                    jitter=0.3,
                    line=dict(width=1),
                    marker=dict(color=colors[het_type], size=4),
                    hoverinfo="y",
                    x=np.repeat(i, len(het_type_df[base_error]))
                    + offset[j],  # x is model_id index + offset
                    # Show legend only for the first appearance of each het_type
                    showlegend=het_type not in legend_items,
                )
            )
            # Add het_type to the set of legend items
            legend_items.add(het_type)
            # After each group of boxes (i.e., for each model_id), add a line
            if (
                j == len(unique_het_types) - 1
            ):  # if this is the last het_type for this model_id
                fig.add_shape(
                    type="line",
                    xref="x",
                    yref="paper",
                    x0=i + 0.5,
                    y0=0,  # place the line half way to the next model_id
                    x1=i + 0.5,
                    y1=1,
                    line=dict(color="white", width=2),
                )

    fig.update_layout(layout)
    fig.update_layout(
        xaxis_title="Models",
        yaxis_title=f"{base_error}-based Relative {letter_code} Reduction",
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(len(unique_model_ids))),
            ticktext=[full_model_names[model_id] for model_id in unique_model_ids],
        ),  # Adjusted this line
        height=600,
        width=800,
        legend=dict(
            x=0.99,
            y=0.01,
            xanchor="right",
            yanchor="bottom",
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    fig.update_layout(yaxis=dict(range=[-1.5, 0.7]))
    fig.update_xaxes(range=[-0.5, len(unique_model_ids) - 0.5])
    pio.write_image(fig, file_name_png)


def create_boxplot_by_het_type(
    metric,
    base_error="MAE",
    selected_norm_level="default",
    selected_norm_type="default",
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(figures_dir, f"box_plot_{metric}_by_het_type.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_scaler_both.csv"))

    # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    df = parse_exp_id(df, inplace=True)
    df = df[~df["model_id"].isin(["Naive", "SNaive"])]

    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    unique_het_types = df["het_type"].unique()
    het_type_order = get_het_type_order()
    full_het_names = get_full_het_names()

    unique_het_types = sorted(unique_het_types, key=lambda x: het_type_order.index(x))
    colors = {
        het_type: het_type_colors[i] for i, het_type in enumerate(unique_het_types)
    }

    fig = go.Figure()
    for het_type in unique_het_types:
        het_type_df = df[df["het_type"] == het_type]
        fig.add_trace(
            go.Box(
                y=het_type_df[base_error],
                name=full_het_names.get(het_type, het_type),
                line=dict(width=1.5),
                marker=dict(color=colors[het_type], size=4),
                boxpoints="all",
                jitter=0.3,
                pointpos=-1.8,
                hoverinfo="y",
            )
        )
    fig.update_layout(layout)
    fig.update_layout(
        xaxis_title="Heterogeneity types",
        yaxis_title=f"{base_error}-based Relative {letter_code} Reduction",
        xaxis=dict(showticklabels=False),
    )
    fig.update_layout(yaxis=dict(range=[-1.4, 0.7]))
    fig.update_layout(height=400, width=800)
    pio.write_image(fig, file_name_png)


def create_boxplot_by_model_id(
    metric,
    base_error="MAE",
    selected_norm_level="default",
    selected_norm_type="default",
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(figures_dir, f"box_plot_{metric}_by_model_id.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_scaler_both.csv"))

    # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    df = parse_exp_id(df, inplace=True)
    df = df[~df["model_id"].isin(["Naive", "SNaive"])]

    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    unique_model_ids = df["model_id"].unique()
    model_id_order = get_model_id_order()
    full_model_names = get_full_model_names()

    unique_model_ids = sorted(unique_model_ids, key=lambda x: model_id_order.index(x))
    colors = {
        model_id: model_id_colors[i] for i, model_id in enumerate(unique_model_ids)
    }
    fig = go.Figure()
    for model_id in unique_model_ids:
        model_id_df = df[df["model_id"] == model_id]
        fig.add_trace(
            go.Box(
                y=model_id_df[base_error],
                name=full_model_names.get(model_id, model_id),
                boxpoints="all",
                jitter=0.3,
                pointpos=-1.8,
                line=dict(width=1.5),
                marker=dict(color=colors[model_id], size=4),
                hoverinfo="y",
            )
        )
    fig.update_layout(layout)
    fig.update_layout(
        xaxis_title="Models",
        yaxis_title=f"{base_error}-based Relative {letter_code} Reduction",
        xaxis=dict(showticklabels=False),
    )
    fig.update_layout(yaxis=dict(range=[-1.2, 0.7]))
    fig.update_layout(height=400, width=800)
    pio.write_image(fig, file_name_png)
