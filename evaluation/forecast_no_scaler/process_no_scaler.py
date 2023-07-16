import os
import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import plotly.subplots as sp
import seaborn as sns


def calculate_scaled_aggregate_MAE():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    results_merged = pd.read_csv(
        os.path.join(tables_dir, "results_raw_no_scaler.csv"),
        dtype={"norm_affine": str},
    )
    ideal_metrics_sampled = pd.read_csv(
        os.path.join(tables_dir, "df_ideal_metrics_sampled.csv"),
        index_col=[0, 1],
        header=[0],
    )
    file_name_csv = os.path.join(tables_dir, "scaled_agg_MAE_no_scaler.csv")
    file_name_xlsx = os.path.join(tables_dir, "scaled_agg_MAE_no_scaler.xlsx")
    df_ideal_error = postprocess_ideal_df(ideal_metrics_sampled)
    df_error = postprocess_forecast_df(results_merged)
    columns_to_divide = ["MAE", "RMSE"]
    average_MAE = df_error[columns_to_divide].div(
        df_ideal_error[columns_to_divide], axis="index"
    )
    average_MAE.to_csv(file_name_csv)
    return average_MAE


def calculate_average_MASE():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    results_indi_merged = pd.read_csv(
        os.path.join(tables_dir, "results_indi_raw_no_scaler.csv")
    )
    ideal_metrics_sampled = pd.read_csv(
        os.path.join(tables_dir, "df_ideal_metrics_sampled.csv"),
        index_col=[0, 1],
        header=[0],
    )
    file_name_csv = os.path.join(tables_dir, "average_MASE_no_scaler.csv")
    file_name_xlsx = os.path.join(tables_dir, "average_MASE_no_scaler.xlsx")
    ideal_metrics_sampled = ideal_metrics_sampled.sort_index()
    df_error = postprocess_results_indi_df(results_indi_merged).sort_index()
    columns_to_divide = ["MAE", "RMSE"]
    average_MASE_per_ID = df_error.div(ideal_metrics_sampled)
    average_MASE = average_MASE_per_ID.groupby(level=0).mean()
    average_MASE.to_csv(file_name_csv)
    return average_MASE


def postprocess_ideal_df(df):
    df = df.groupby(level=0).mean()
    return df


def postprocess_forecast_df(df):
    df_filtered = df[["exp_id", "MAE", "RMSE"]]
    df_filtered = df_filtered.set_index("exp_id")
    return df_filtered


def postprocess_results_indi_df(original_df):
    df = original_df.copy()
    df = df[df["ID"] != "ALL"]
    df.loc[:, "ID"] = df["ID"].astype(int)
    df_filtered = df[["exp_id", "ID", "MAE", "RMSE"]]
    df_filtered = df_filtered.set_index(["exp_id", "ID"])
    return df_filtered


def split_words(s):
    if "structural_break" in s:
        parts = s.split("structural_break")
        word1 = parts[0].rstrip("_")
        word2 = "structural_break"
        word3 = parts[1].lstrip("_")
    else:
        word1, word2, word3 = s.rsplit("_", 2)
    return pd.Series([word1, word2, word3])


def plot_sampled_error():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    figure_dir = os.path.join(parent_dir, "figures")
    scaled_agg_MAE_no_scaler = pd.read_csv(
        os.path.join(tables_dir, "scaled_agg_MAE_no_scaler.csv"), index_col=0
    )
    scaled_agg_MAE_no_scaler.reset_index(inplace=True)
    averge_MASE_no_scaler = pd.read_csv(
        os.path.join(tables_dir, "average_MASE_no_scaler.csv"), index_col=0
    )
    averge_MASE_no_scaler.reset_index(inplace=True)

    # Split the index column into three new columns
    scaled_agg_MAE_no_scaler[
        ["model_id", "het_type", "het_strength"]
    ] = scaled_agg_MAE_no_scaler["exp_id"].apply(split_words)
    scaled_agg_MAE_no_scaler.drop(columns="exp_id", inplace=True)
    scaled_agg_MAE_no_scaler["het_strength"] = pd.to_numeric(
        scaled_agg_MAE_no_scaler["het_strength"]
    )
    averge_MASE_no_scaler[
        ["model_id", "het_type", "het_strength"]
    ] = averge_MASE_no_scaler["exp_id"].apply(split_words)
    averge_MASE_no_scaler.drop(columns="exp_id", inplace=True)
    averge_MASE_no_scaler["het_strength"] = pd.to_numeric(
        averge_MASE_no_scaler["het_strength"]
    )

    # Define a color dictionary
    color_dict = {
        "TP": "#1f78b4",
        "TP_localST": "#33a02c",
        "NP": "#fdbf6f",
        "NP_localST": "#ff7f00",
        "NP_FNN": "#6a3d9a",
        "RNN": "#b15928",
        "TF": "#a6cee3",
        "LGBM": "#b2df8a",
        "NP_FNN_sw": "#ffc0cb",
    }
    line_dict = {
        "amplitude": 2.5,
        "offset": 2.5,
        "trend": 2.5,
        "heteroscedasticity": 2.5,
        "structural_break": 2.5,
    }

    for metric, df in [
        ("scaled_agg_MAE_no_scaler", scaled_agg_MAE_no_scaler),
        ("average_MASE_no_scaler", averge_MASE_no_scaler),
    ]:
        df = df[
            ~df["model_id"].isin(["Naive", "SNaive"])
        ]  # exclude 'Naive' and 'SNaive' models
        grouped = df.groupby("het_type")

        fig = sp.make_subplots(
            rows=1, cols=len(grouped), subplot_titles=list(grouped.groups.keys())
        )  # arrange subplots in columns

        for i, (het_type, group) in enumerate(grouped):
            show_legend = i == 0
            for model_id in group["model_id"].unique():
                subgroup = group[group["model_id"] == model_id]
                subgroup = subgroup.sort_values("het_strength")
                fig.add_trace(
                    go.Scatter(
                        x=subgroup["het_strength"],
                        y=subgroup["MAE"],
                        showlegend=show_legend,
                        mode="lines",
                        name=f"{model_id}",
                        line=dict(color=color_dict[model_id]),
                    ),
                    row=1,
                    col=i + 1,
                )
            fig.add_shape(
                type="line",
                x0=min(subgroup["het_strength"]),
                x1=max(subgroup["het_strength"]),
                y0=line_dict[het_type],
                y1=line_dict[het_type],
                line=dict(color="Red", width=2, dash="dot"),
                row=1,
                col=i + 1,
            )
            fig.update_yaxes(
                range=[1, 6], row=1, col=i + 1
            )  # specify y-axis range for each subplot

        fig.update_layout(height=800, width=400 * len(grouped), title_text=f"{metric}")
        fig.update_layout(
            legend=dict(
                x=1,  # This sets the x position of the legend
                y=0.99,  # This sets the y position of the legend
                traceorder="normal",
                font=dict(family="sans-serif", size=12, color="black"),
            )
        )
        fig.write_image(
            os.path.join(figure_dir, f"{metric}_faceted_line_charts.png")
        )  # Save the figure


def find_first_exceeding_threshold():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")

    # Load the same data
    scaled_agg_MAE_no_scaler = pd.read_csv(
        os.path.join(tables_dir, "scaled_agg_MAE_no_scaler.csv"), index_col=0
    )
    scaled_agg_MAE_no_scaler.reset_index(inplace=True)
    averge_MASE_no_scaler = pd.read_csv(
        os.path.join(tables_dir, "average_MASE_no_scaler.csv"), index_col=0
    )
    averge_MASE_no_scaler.reset_index(inplace=True)

    # Do the same preprocessing
    scaled_agg_MAE_no_scaler[
        ["model_id", "het_type", "het_strength"]
    ] = scaled_agg_MAE_no_scaler["exp_id"].apply(split_words)
    scaled_agg_MAE_no_scaler.drop(columns="exp_id", inplace=True)
    scaled_agg_MAE_no_scaler["het_strength"] = pd.to_numeric(
        scaled_agg_MAE_no_scaler["het_strength"]
    )
    averge_MASE_no_scaler[
        ["model_id", "het_type", "het_strength"]
    ] = averge_MASE_no_scaler["exp_id"].apply(split_words)
    averge_MASE_no_scaler.drop(columns="exp_id", inplace=True)
    averge_MASE_no_scaler["het_strength"] = pd.to_numeric(
        averge_MASE_no_scaler["het_strength"]
    )

    # Initialize an empty DataFrame to store the results
    results = pd.DataFrame()

    # Find the first exceeding value for both metrics
    for metric, df in [
        ("scaled_agg_MAE_no_scaler", scaled_agg_MAE_no_scaler),
        ("average_MASE_no_scaler", averge_MASE_no_scaler),
    ]:
        df = df[
            ~df["model_id"].isin(["Naive", "SNaive"])
        ]  # exclude 'Naive' and 'SNaive' models
        grouped = df.groupby(["het_type", "model_id"])

        for (het_type, model_id), group in grouped:
            group = group.sort_values("het_strength")
            exceeding = group[group["MAE"] > 2.5]
            if not exceeding.empty:
                first_exceeding = exceeding.iloc[0]
                new_data = pd.DataFrame(
                    {
                        "Metric": [metric],
                        "HetType": [het_type],
                        "ModelId": [model_id],
                        "HetStrength": [first_exceeding["het_strength"]],
                        "Error": [first_exceeding["MAE"]],
                    }
                )

                results = pd.concat([results, new_data], ignore_index=True)

    file_name_csv = os.path.join(tables_dir, "problematic_candidates.csv")
    results.to_csv(file_name_csv)
