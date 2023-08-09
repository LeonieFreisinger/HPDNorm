import os
import pathlib

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


from evaluation.helpers.layout import create_layout

layout, het_type_colors, model_id_colors, dataset_colors = create_layout()


from evaluation.helpers.params import (get_full_het_names,
                                       get_full_model_names,
                                       get_het_type_order, 
                                       get_model_id_order,
                                       get_full_norm_names,
                                       )


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
    file_name_png = os.path.join(figures_dir, f"box_plots_all_{metric}.png")
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
                    boxpoints="outliers",
                    # jitter=0.3,
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
        yaxis_title=f"RER of {base_error}-based {letter_code}",
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
    fig.update_layout(
        autosize=False,
        margin=dict(
            l=5,  # left margin
            r=5,  # right margin
            b=20,  # bottom margin
            t=40,  # top margin
            pad=1  # padding
        )
    )
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
                boxpoints="outliers",
                # jitter=0.3,
                # pointpos=-1.8,
                hoverinfo="y",
            )
        )
    fig.update_layout(layout)
    fig.update_layout(
        xaxis_title="Heterogeneity types",
        yaxis_title=f"RER of {base_error}-based {letter_code}",
        xaxis=dict(showticklabels=False),
    )
    fig.update_layout(yaxis=dict(range=[-1.4, 0.7]))
    fig.update_layout(height=400, width=800)
    fig.update_layout(
        autosize=False,
        margin=dict(
            l=5,  # left margin
            r=5,  # right margin
            b=20,  # bottom margin
            t=40,  # top margin
            pad=1  # padding
        )
    )
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
                boxpoints="outliers",
                # jitter=0.3,
                # pointpos=-1.8,
                line=dict(width=1.5),
                marker=dict(color=colors[model_id], size=4),
                hoverinfo="y",
            )
        )
    fig.update_layout(layout)
    fig.update_layout(
        xaxis_title="Models",
        yaxis_title=f"RER of {base_error}-based {letter_code}",
        xaxis=dict(showticklabels=False),
    )
    fig.update_layout(yaxis=dict(range=[-1.2, 0.7]))
    fig.update_layout(height=400, width=800)
    fig.update_layout(
        autosize=False,
        margin=dict(
            l=5,  # left margin
            r=5,  # right margin
            b=20,  # bottom margin
            t=40,  # top margin
            pad=1  # padding
        )
    )
    pio.write_image(fig, file_name_png)


def create_boxplot_aggregated(
    metric,
    base_error="MAE",
    selected_norm_level="default",
    selected_norm_type="default",
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(figures_dir, f"box_plot_{metric}_aggregated.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_scaler_both.csv"))

    # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    df = parse_exp_id(df, inplace=True)
    df = df[~df["model_id"].isin(["Naive", "SNaive"])]

    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    # unique_het_types = df["het_type"].unique()
    # het_type_order = get_het_type_order()
    # full_het_names = get_full_het_names()

    # unique_het_types = sorted(unique_het_types, key=lambda x: het_type_order.index(x))
    # colors = {
    #     het_type: het_type_colors[i] for i, het_type in enumerate(unique_het_types)
    # }

    fig = go.Figure()

    fig.add_trace(
            go.Box(
                y=df[base_error],
                name="All Het Types",
                line=dict(width=1.5),
                # Adjust these properties as you wish:
                marker=dict(size=4),
                boxpoints="outliers",
                hoverinfo="y",
            )
        )
    # for het_type in unique_het_types:
    #     het_type_df = df[df["het_type"] == het_type]
    #     fig.add_trace(
    #         go.Box(
    #             y=het_type_df[base_error],
    #             name=full_het_names.get(het_type, het_type),
    #             line=dict(width=1.5),
    #             marker=dict(color=colors[het_type], size=4),
    #             boxpoints="outliers",
    #             # jitter=0.3,
    #             # pointpos=-1.8,
    #             hoverinfo="y",
    #         )
    #     )
    fig.update_layout(layout)
    fig.update_layout(
        # # xaxis_title="Heterogeneity types",
        yaxis_title=f"RER of {base_error}-based {letter_code}",
        xaxis=dict(showticklabels=False),
    )
    fig.update_layout(yaxis=dict(range=[-2.5, 1.2 ])) #-2.5, 1.2 
    fig.update_layout(height=600, width=300)
    fig.update_layout(
        autosize=False,
        margin=dict(
            l=5,  # left margin
            r=5,  # right margin
            b=20,  # bottom margin
            t=40,  # top margin
            pad=1  # padding
        )
    )
    pio.write_image(fig, file_name_png)

def create_grouped_box_plots_per_norm_type(metric, base_error="MAE"):
    # loading and preprocessing the dataframe as before
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(figures_dir, f"bar_plot_{metric}_by_norm_type.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_scaler_both.csv"))

    # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    df = parse_exp_id(df, inplace=True)
    df = df[~df["model_id"].isin(["Naive", "SNaive"])]
    df = df[df["type"] != "None"]

    # if selected_norm_level != "default":
    #     df = df[df["level"].isin(selected_norm_level)]
    # if selected_norm_type != "default":
    #     df = df[df["type"].isin(selected_norm_type)]

    # Creating a new column that combines 'type' and 'level' for grouping
    df['type_level'] = df['type'].astype(str) + "_" + df['level'].astype(str)

    
    model_id_order = get_model_id_order()
    full_model_names = get_full_model_names()
    full_norm_names = get_full_norm_names()

    # Create a new list of type_levels based on the predefined order in your dictionary
    unique_type_levels = sorted(df['type_level'].unique(), key=lambda x: list(full_norm_names.keys()).index(x))


    # Get unique model_ids and their order
    unique_model_ids = df["model_id"].unique()

    # Sort unique_model_ids according to their order
    unique_model_ids = sorted(unique_model_ids, key=lambda x: model_id_order.index(x))
    # Specify different colors for different model_ids
    colors = {model_id: model_id_colors[i] for i, model_id in enumerate(unique_model_ids)}

    added_names = set()

    # Create subplots, with one column for each type_level
    fig = go.Figure()

    for i, type_level in enumerate(unique_type_levels):
        # Filter dataframe for each type_level
        type_level_df = df[df['type_level'] == type_level]

        for model_id in unique_model_ids:
            # Get the rows for the current model_id and average the base_error
            model_id_df = type_level_df[type_level_df["model_id"] == model_id]
            average_base_error = model_id_df[base_error].mean()
            
            # Add a boxplot for each model_id for the specific type_level
            fig.add_trace(
                go.Box(
                    y=[average_base_error],
                    name=full_model_names[model_id],
                    marker=dict(color=colors[model_id], size=4),
                    hoverinfo="y",
                    x=[full_norm_names[type_level]],
                    showlegend = full_model_names[model_id] not in added_names,
                )
            )
            added_names.add(full_model_names[model_id])

    fig.update_layout(
        xaxis_title="Normalization Methods",
        yaxis_title=f"RER of {base_error}-based {letter_code}",
        xaxis=dict(
            type='category',
            categoryorder='array', 
            categoryarray=unique_type_levels
        ),
        height=600,
        width=700,
        legend=dict(x=1, y=1, xanchor="left", yanchor="top", bgcolor="rgba(0,0,0,0)")
    )
    fig.update_layout(yaxis=dict(range=[-0.5, 0.7]))
    fig.update_layout(
        autosize=False,
        margin=dict(
            l=5,  # left margin
            r=5,  # right margin
            b=20,  # bottom margin
            t=20,  # top margin
            pad=1  # padding
        )
    )

    pio.write_image(fig, file_name_png)

def create_grouped_box_plots_per_norm_type_indi(metric, base_error="MAE"):
    # loading and preprocessing the dataframe as before
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(figures_dir, f"bar_plot_{metric}_by_norm_type_indi.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_scaler_both.csv"))

        # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    df = parse_exp_id(df, inplace=True)
    df = df[~df["model_id"].isin(["Naive", "SNaive"])]
    df = df[df["type"] != "None"]

    df['type_level'] = df['type'].astype(str) + "_" + df['level'].astype(str)

    # Get unique model_ids and their order
    
    model_id_order = get_model_id_order()
    full_model_names = get_full_model_names()
    full_het_type_names = get_full_het_names()
    full_norm_names = get_full_norm_names()

    # Create a new list of type_levels based on the predefined order in your dictionary
    unique_type_levels = sorted(df['type_level'].unique(), key=lambda x: list(full_norm_names.keys()).index(x))
    unique_model_ids = df["model_id"].unique()

    unique_model_ids = sorted(unique_model_ids, key=lambda x: model_id_order.index(x))
    colors = {model_id: model_id_colors[i] for i, model_id in enumerate(unique_model_ids)}

    # Get unique het_types
    unique_het_types = df['het_type'].unique()
    
    
    # Create subplots, with one row for each het_type
    fig = make_subplots(rows=len(unique_het_types), cols=1, vertical_spacing=0.01)

    # Set a flag to ensure the legend is added only once
    legend_added = False

    # Iterate over each unique het_type
    for row, het_type in enumerate(unique_het_types, start=1):
        # Filter the dataframe for the current het_type
        df_het_type = df[df['het_type'] == het_type]
        df_het_type.sort_values(['type_level'], inplace=True)
        print(df_het_type)
        # Get the unique type_levels for the current het_type
        # unique_type_levels = df_het_type['type_level'].unique()

    # Initialize an empty set to keep track of the model names that have been added to the legend
    added_names = set()

    # Iterate over each unique het_type
    for row, het_type in enumerate(unique_het_types, start=1):
        # Filter the dataframe for the current het_type
        df_het_type = df[df['het_type'] == het_type]

        # Get the unique type_levels for the current het_type
        # unique_type_levels = df_het_type['type_level'].unique()

        for i, type_level in enumerate(unique_type_levels):
            # Filter the dataframe for the current type_level
            df_type_level = df_het_type[df_het_type['type_level'] == type_level]

            for model_id in unique_model_ids:
                # Get the rows for the current model_id
                df_model_id = df_type_level[df_type_level["model_id"] == model_id]

                # Add a boxplot for each model_id for the specific type_level
                fig.add_trace(
                    go.Box(
                        y=df_model_id[base_error],
                        name=full_model_names[model_id],
                        marker=dict(color=colors[model_id], size=2),
                        hoverinfo="y",
                        x=[full_norm_names[type_level]]*len(df_model_id),
                        showlegend= (full_model_names[model_id] not in added_names),
                    ),
                    row=row,
                    col=1
                )
                added_names.add(full_model_names[model_id])

        # Add the het_type as a title for each subplot, rotated by 90 degrees
        unique_het_types_full = [full_het_type_names.get(het_type, het_type) for het_type in unique_het_types]
        fig.add_annotation(
            text=unique_het_types_full[row-1],
            xref='paper',
            yref='paper',
            x=-0.14,  # adjust as necessary
            y=(len(unique_het_types) - row) / len(unique_het_types) + 0.5 / len(unique_het_types),  # position the text in the middle of each subplot's y axis
            showarrow=False,
            font=dict(size=14),
            textangle=-90,
            xanchor='left',
            yanchor='middle'
        )

        # Update the xaxis labels only for the last subplot row
        if row == len(unique_het_types):
            fig.update_xaxes(title_text="Normalization Methods", row=row, col=1, showticklabels=True)
        else:
            fig.update_xaxes(showticklabels=False, row=row, col=1)
    

        # Once all traces for the first row are added, update the flag
        legend_added = True
    fig.update_yaxes(title_text=f"RER of {base_error}-based {letter_code}", row=3, col=1)
    fig.update_yaxes(range=[-0.5, 0.7], title_standoff = 35)
    fig.update_layout(
        height=170 * len(unique_het_types),  # adjust the figure height based on the number of subplots
        width=700,
        legend=dict(x=1, y=1, xanchor="left", yanchor="top", bgcolor="rgba(0,0,0,0)"),
        yaxis=dict(range=[-1.5, 0.7])
    )
    fig.update_layout(
            autosize=False,
            margin=dict(
                l=5,  # left margin
                r=5,  # right margin
                b=20,  # bottom margin
                t=20,  # top margin
                pad=1  # padding
            )
        )

    pio.write_image(fig, file_name_png)


def create_grouped_box_plots_compare_level(metric, base_error="MAE"):
        # loading and preprocessing the dataframe as before
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(figures_dir, f"box_plot_{metric}_by_level.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_scaler_both.csv"))

    # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    df = parse_exp_id(df, inplace=True)
    df = df[~df["model_id"].isin(["Naive", "SNaive"])]
    df = df[df["type"] != "None"]

    # if selected_norm_level != "default":
    #     df = df[df["level"].isin(selected_norm_level)]
    # if selected_norm_type != "default":
    #     df = df[df["type"].isin(selected_norm_type)]

    # Creating a new column that combines 'type' and 'level' for grouping
    df['type_level'] = df['type'].astype(str) + "_" + df['level'].astype(str)

    
    model_id_order = get_model_id_order()
    full_model_names = get_full_model_names()
    full_norm_names = get_full_norm_names()

    # Create a new list of type_levels based on the predefined order in your dictionary
    unique_type_levels = sorted(df['type_level'].unique(), key=lambda x: list(full_norm_names.keys()).index(x))


    # Get unique model_ids and their order
    unique_model_ids = df["model_id"].unique()

    # Sort unique_model_ids according to their order
    unique_model_ids = sorted(unique_model_ids, key=lambda x: model_id_order.index(x))
    # Specify different colors for different model_ids
    colors = {model_id: model_id_colors[i] for i, model_id in enumerate(unique_model_ids)}

    added_names = set()

    # Create subplots, with one column for each type_level
    fig = go.Figure()

    # for i, type_level in enumerate(unique_type_levels):
    #     # Filter dataframe for each type_level
    #     type_level_df = df[df['type_level'] == type_level]

    #     for model_id in unique_model_ids:
    #         # Get the rows for the current model_id and average the base_error
    #         model_id_df = type_level_df[type_level_df["model_id"] == model_id]
    #         average_base_error = model_id_df[base_error].mean()
            
    #         # Add a boxplot for each model_id for the specific type_level
    #         fig.add_trace(
    #             go.Box(
    #                 y=[average_base_error],
    #                 name=full_model_names[model_id],
    #                 marker=dict(color=colors[model_id], size=4),
    #                 hoverinfo="y",
    #                 x=[full_norm_names[type_level]],
    #                 showlegend = full_model_names[model_id] not in added_names,
    #             )
    #         )
    #         added_names.add(full_model_names[model_id])

    # Lists to store average base errors for both categories
    errors_per_time_series_or_instance = []
    errors_per_dataset_or_batch = []

    # Loop through unique type levels and model IDs
    for type_level in unique_type_levels:
        for model_id in unique_model_ids:
            # Filter dataframe for current type_level and model_id
            model_type_df = df[(df['type_level'] == type_level) & (df['model_id'] == model_id)]
            average_base_error = model_type_df[base_error].mean()
            
            # Categorize the average base error based on type_level strings
            if 'per_time_series' in type_level or 'instance' in type_level:
                errors_per_time_series_or_instance.append(average_base_error)
            elif 'per_dataset' in type_level or 'batch' in type_level:
                errors_per_dataset_or_batch.append(average_base_error)

    # Add the two boxplots
    # First boxplot: for 'per_time_series' or 'instance'
    fig.add_trace(
        go.Box(
            y=errors_per_time_series_or_instance,
            # name="Per Time Series / Instance",
            marker=dict(color='blue', size=4),
            hoverinfo="y",
            showlegend=True,
        )
    )

    # Second boxplot: for 'per_dataset' or 'batch'
    fig.add_trace(
        go.Box(
            y=errors_per_dataset_or_batch,
            # name="Per Dataset / Batch",
            marker=dict(color='blue', size=4),
            hoverinfo="y",
            showlegend=True,
        )
    )
    
    fig.update_layout(
        xaxis_title="Normalization Methods",
        yaxis_title=f"RER of {base_error}-based {letter_code}",
        xaxis=dict(
            type='category',
            categoryorder='array', 
            categoryarray=unique_type_levels
        ),
        height=600,
        width=700,
        legend=dict(x=1, y=1, xanchor="left", yanchor="top", bgcolor="rgba(0,0,0,0)")
    )
    fig.update_layout(yaxis=dict(range=[-0.5, 0.7]))
    fig.update_layout(
        autosize=False,
        margin=dict(
            l=5,  # left margin
            r=5,  # right margin
            b=20,  # bottom margin
            t=20,  # top margin
            pad=1  # padding
        )
    )

    pio.write_image(fig, file_name_png)