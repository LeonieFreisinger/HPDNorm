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
                                       get_full_dataset_names,
                                       get_full_norm_names,
                                       
                                       )


def create_faceted_box_plots(
    metric,
    base_error="MAE",
    selected_norm_level="default",
    selected_norm_type="default",
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(figures_dir, f"box_plots_all_{metric}_real_world.png")
    df = pd.read_csv(
        os.path.join(tables_dir, f"{metric}_rel_to_no_real_world_both.csv"),
    )
    # file_name_png = os.path.join(figures_dir, f"box_plots_all_{metric}_real_world.png") # without window_based
    # df = pd.read_csv(
    #     os.path.join(tables_dir, f"rel_to_no_scaler_{metric}_real_world_both.csv"),
    # )

    # Generate relevant cols model_id, het_type, het_strength
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    df = df.rename(columns={'scaler': 'type', 'scaling_level': 'level', 'exp_id': 'dataset'})

    # remove normalization type and level, that has not been selected
    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    # print(df)
    # Get unique exp_ids
    unique_datasets = df["dataset"].unique()
    unique_model_ids = df["model_id"].unique()

    model_id_order = get_model_id_order()
    # het_type_order = get_het_type_order()
    full_model_names = get_full_model_names()
    full_dataset_names = get_full_dataset_names()

    # Sort unique_model_ids and unique_het_types according to their respective orders
    unique_model_ids = sorted(unique_model_ids, key=lambda x: model_id_order.index(x))

    # Specify different colors for different het_types
    colors = {
        dataset: dataset_colors[i] for i, dataset in enumerate(unique_datasets)
    }

    # Create subplots, with one column for each model_id
    fig = (
        go.Figure()
    )  

    offset = np.linspace(-0.3, 0.3, len(unique_datasets))
    # Initialize an empty set to keep track of legend items
    legend_items = set()

    for i, model_id in enumerate(unique_model_ids):
        for j, dataset in enumerate(unique_datasets):
            # Filter dataframe for each het_type and model_id
            dataset_df = df[
                (df["model_id"] == model_id) & (df["dataset"] == dataset)
            ]

            # Add a boxplot for each het_type for the specific model_id
            fig.add_trace(
                go.Box(
                    y=dataset_df[base_error],
                    name=full_dataset_names[dataset],
                    legendgroup=dataset,
                    boxpoints="outliers",
                    # jitter=0.3,
                    line=dict(width=1),
                    marker=dict(color=colors[dataset], size=4),
                    hoverinfo="y",
                    x=np.repeat(i, len(dataset_df[base_error]))
                    + offset[j],  # x is model_id index + offset
                    # Show legend only for the first appearance of each het_type
                    showlegend=dataset not in legend_items,
                )
            )
            # Add het_type to the set of legend items
            legend_items.add(dataset)
            # After each group of boxes (i.e., for each model_id), add a line
            if (
                j == len(unique_datasets) - 1
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
        width=730,
        legend=dict(
            x=1,
            y=1,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    fig.update_layout(yaxis=dict(range=[-2.5, 1.2]))
    fig.update_xaxes(range=[-0.5, len(unique_model_ids) - 0.5], title_standoff = 30)
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



def create_boxplot_by_model_id(
    metric,
    base_error="MAE",
    selected_norm_level="default",
    selected_norm_type="default",
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(figures_dir, f"box_plot_{metric}_by_model_id_real_world.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_real_world_both.csv"))

    # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    # df = parse_exp_id(df, inplace=True)
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
    # fig.update_xaxes(title_standoff = 30)
    fig.update_layout(yaxis=dict(range=[-2.5, 1.2]))
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



def create_boxplot_by_dataset(
    metric,
    base_error="MAE",
    selected_norm_level="default",
    selected_norm_type="default",
):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figures_dir = os.path.join(parent_dir, "figures")
    file_name_png = os.path.join(figures_dir, f"box_plot_{metric}_by_dataset_real_world.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_real_world_both.csv"))

    # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    # df = parse_exp_id(df, inplace=True)
    df = df[~df["model_id"].isin(["Naive", "SNaive"])]

    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    unique_datasets = df["exp_id"].unique()
    # dataset_order = get_het_type_order()
    full_dataset_names = get_full_dataset_names()

    # unique_datasets = sorted(unique_datasets, key=lambda x: dataset_order.index(x))
    colors = {
        dataset: dataset_colors[i] for i, dataset in enumerate(unique_datasets)
    }

    fig = go.Figure()
    for dataset in unique_datasets:
        dataset_df = df[df["exp_id"] == dataset]
        fig.add_trace(
            go.Box(
                y=dataset_df[base_error],
                name=full_dataset_names[dataset],
                line=dict(width=1.5),
                marker=dict(color=colors[dataset], size=4),
                boxpoints="outliers",
                # jitter=0.3,
                # pointpos=-1.8,
                hoverinfo="y",
            )
        )
    fig.update_layout(layout)
    fig.update_layout(
        xaxis_title="Datasets",
        yaxis_title=f"RER of {base_error}-based {letter_code}",
        xaxis=dict(showticklabels=False),
    )
    fig.update_layout(yaxis=dict(range=[-2.5, 1.2]))
    # fig.update_xaxes(title_standoff = 30)
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
    file_name_png = os.path.join(figures_dir, f"box_plot_{metric}_aggregated_real_world.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_real_world_both.csv"))

    # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    # df = parse_exp_id(df, inplace=True)
    df = df[~df["model_id"].isin(["Naive", "SNaive"])]

    if selected_norm_level != "default":
        df = df[df["level"].isin(selected_norm_level)]
    if selected_norm_type != "default":
        df = df[df["type"].isin(selected_norm_type)]

    
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
    fig.update_layout(layout)
    fig.update_layout(
        # xaxis_title="Models",
        yaxis_title=f"RER of {base_error}-based {letter_code}",
        xaxis=dict(showticklabels=False),
    )
    # fig.update_xaxes(title_standoff = 30)
    fig.update_layout(yaxis=dict(range=[-2.5, 1.2]))
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
    file_name_png = os.path.join(figures_dir, f"bar_plot_{metric}_real_world_by_norm_type.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_real_world_both.csv"))

    # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
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
        width=650,
        legend=dict(x=1, y=1, xanchor="left", yanchor="top", bgcolor="rgba(0,0,0,0)")
    )
    fig.update_layout(yaxis=dict(range=[-2.5, 1.2]))
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
    file_name_png = os.path.join(figures_dir, f"bar_plot_{metric}_real_world_by_norm_type_indi.png")
    df = pd.read_csv(os.path.join(tables_dir, f"{metric}_rel_to_no_real_world_both.csv"))

        # Process DataFrame
    letter_code = "AISE" if metric == "average_MASE" else "ISAE"
    df = df[~df["model_id"].isin(["Naive", "SNaive"])]
    df = df[df["type"] != "None"]

    df['type_level'] = df['type'].astype(str) + "_" + df['level'].astype(str)

    # Get unique model_ids and their order
    
    model_id_order = get_model_id_order()
    full_model_names = get_full_model_names()
    full_het_type_names = get_full_het_names()
    full_norm_names = get_full_norm_names()
    full_dataset_names = get_full_dataset_names()

    # Create a new list of type_levels based on the predefined order in your dictionary
    unique_type_levels = sorted(df['type_level'].unique(), key=lambda x: list(full_norm_names.keys()).index(x))
    unique_model_ids = df["model_id"].unique()

    unique_model_ids = sorted(unique_model_ids, key=lambda x: model_id_order.index(x))
    colors = {model_id: model_id_colors[i] for i, model_id in enumerate(unique_model_ids)}

    # Get unique het_types
    unique_datasets = df['exp_id'].unique()
    
    
    # Create subplots, with one row for each het_type
    fig = make_subplots(rows=len(unique_datasets), cols=1, vertical_spacing=0.045)

    # Set a flag to ensure the legend is added only once
    legend_added = False
    # Initialize an empty set to keep track of the model names that have been added to the legend
    added_names = set()

    # Iterate over each unique het_type
    for row, dataset in enumerate(unique_datasets, start=1):
        # Filter the dataframe for the current het_type
        df_dataset= df[df['exp_id'] == dataset]
        df_dataset.sort_values(['type_level'], inplace=True)

        for i, type_level in enumerate(unique_type_levels):
            # Filter the dataframe for the current type_level
            df_type_level = df_dataset[df_dataset['type_level'] == type_level]

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

        # Add the dataset as a title for each subplot, rotated by 90 degrees
        unique_datasets_full = [full_dataset_names.get(dataset, dataset) for dataset in unique_datasets]
        fig.add_annotation(
            text=unique_datasets_full[row-1],
            xref='paper',
            yref='paper',
            x=-0.1,  # adjust as necessary
            y=(len(unique_datasets) - row) / len(unique_datasets) + 0.5 / len(unique_datasets),  # position the text in the middle of each subplot's y axis
            showarrow=False,
            font=dict(size=14),
            textangle=-90,
            xanchor='left',
            yanchor='middle'
        )

        # Update the xaxis labels only for the last subplot row
        if row == len(unique_datasets):
            fig.update_xaxes(title_text="Normalization Methods", row=row, col=1, showticklabels=True)
        else:
            fig.update_xaxes(showticklabels=False, row=row, col=1)
    

        # Once all traces for the first row are added, update the flag
        legend_added = True
    fig.update_yaxes(title_text=f"RER of {base_error}-based {letter_code}", row=3, col=1,title_standoff = 30 )
    fig.update_yaxes(range=[-2.5, 1.2])
    fig.update_layout(
        height=120 * len(unique_datasets),  # adjust the figure height based on the number of subplots
        width=650,
        legend=dict(x=1, y=1, xanchor="left", yanchor="top", bgcolor="rgba(0,0,0,0)"),
        # yaxis=dict(range=[-2.5, 1.2])
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