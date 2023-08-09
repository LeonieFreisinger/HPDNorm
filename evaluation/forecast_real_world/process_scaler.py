import os
import pathlib

import pandas as pd


def postprocess_results_indi_df(original_df):
    df = original_df.copy()
    df = df[df["ID"] != "ALL"]
    # df.loc[:, "ID"] = df["ID"].astype(int)
    df_filtered = df[
        ["exp_id", "ID", "MAE", "RMSE", "scaler", "scaling_level", "model_id"]
    ]
    return df_filtered


def calculate_average_MASE():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    results_indi_merged = pd.read_csv(
        os.path.join(tables_dir, "results_indi_real_world.csv")
    )
    file_name_csv = os.path.join(tables_dir, "average_MASE_real_world.csv")
    df_error = results_indi_merged[
        ~results_indi_merged["model_id"].isin(["Naive", "SNaive"])
    ]
    df_ideal_error = results_indi_merged[results_indi_merged["model_id"] == "Naive"]

    # Filter rows in ideal_metrics_sampled where the multi-index matches
    filtered_df_ideal_error = df_ideal_error  # [df_ideal_error.index.isin(idx)]
    # print(filtered_df_ideal_error)
    df_error = postprocess_results_indi_df(df_error)
    filtered_df_ideal_error = postprocess_results_indi_df(filtered_df_ideal_error)

    filtered_df_ideal_error[
        ["ID", "exp_id", "scaler", "scaling_level"]
    ] = filtered_df_ideal_error[["ID", "exp_id", "scaler", "scaling_level"]].astype(str)
    filtered_df_ideal_error.set_index(
        ["ID", "exp_id", "scaler", "scaling_level"], inplace=True
    )

    df_error[["ID", "exp_id", "scaler", "scaling_level"]] = df_error[
        ["ID", "exp_id", "scaler", "scaling_level"]
    ].astype(str)
    df_error.set_index(["ID", "exp_id", "scaler", "scaling_level"], inplace=True)

    filtered_df_ideal_error.sort_index(inplace=True)
    df_error.sort_index(inplace=True)


    # Create a new DataFrame for division operation
    div_result = (
        df_error[["MAE", "RMSE"]]
        .div(filtered_df_ideal_error[["MAE", "RMSE"]])
    )
    div_result.reset_index(inplace=True)
    df_error.reset_index(inplace=True)

    # Concat other columns from df_error
    average_MASE_per_ID = pd.concat([div_result, df_error[["model_id"]]], axis=1)
    # average_MASE = average_MASE_per_ID
    average_MASE = average_MASE_per_ID.groupby(
        ["exp_id","scaler", "scaling_level", "model_id" ]
    ).mean()
    average_MASE.to_csv(file_name_csv)


def calculate_scaled_agg_MAE():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    results_indi_merged = pd.read_csv(
        os.path.join(tables_dir, "results_indi_real_world.csv")
    )
    file_name_csv = os.path.join(tables_dir, "scaled_agg_MAE_real_world.csv")
    df_error = results_indi_merged[
        ~results_indi_merged["model_id"].isin(["Naive", "SNaive"])
    ]
    df_ideal_error = results_indi_merged[results_indi_merged["model_id"] == "Naive"]

    # Filter rows in ideal_metrics_sampled where the multi-index matches
    filtered_df_ideal_error = df_ideal_error  # [df_ideal_error.index.isin(idx)]
    # print(filtered_df_ideal_error)
    df_error = postprocess_results_indi_df(df_error)
    filtered_df_ideal_error = postprocess_results_indi_df(filtered_df_ideal_error)

    filtered_df_ideal_error[
        ["ID", "exp_id", "scaler", "scaling_level"]
    ] = filtered_df_ideal_error[["ID", "exp_id", "scaler", "scaling_level"]].astype(str)
    filtered_df_ideal_error.set_index(
        ["ID", "exp_id", "scaler", "scaling_level"], inplace=True
    )

    df_error[["ID", "exp_id", "scaler", "scaling_level"]] = df_error[
        ["ID", "exp_id", "scaler", "scaling_level"]
    ].astype(str)
    df_error.set_index(["ID", "exp_id", "scaler", "scaling_level"], inplace=True)

    filtered_df_ideal_error.sort_index(inplace=True)
    df_error.sort_index(inplace=True)
    filtered_df_ideal_error.reset_index(inplace=True)
    df_error.reset_index(inplace=True)

    # create both avg errors
    filtered_df_ideal_error_mean = filtered_df_ideal_error.groupby(
        ["exp_id","scaler", "scaling_level", "model_id" ]
    ).mean()
    df_error_mean = df_error.groupby(
        ["exp_id","scaler", "scaling_level", "model_id" ]
    ).mean()

    filtered_df_ideal_error_mean.reset_index(level=3, inplace=True)
    df_error_mean.reset_index(level=3, inplace=True)

    # Create a new DataFrame for division operation
    div_result = (
        df_error_mean[["MAE", "RMSE"]]
        .div(filtered_df_ideal_error_mean[["MAE", "RMSE"]])
    )
    div_result.reset_index(inplace=True)
    df_error_mean.reset_index(inplace=True)

    # Concat other columns from df_error
    scaled_agg_MAE = pd.concat([div_result, df_error_mean[["model_id"]]], axis=1)
    
    scaled_agg_MAE.set_index(["exp_id"], inplace=True)
    scaled_agg_MAE.to_csv(file_name_csv)


def calculate_error_rel_to_no_scaler_for_metric(metric):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    if metric == "average_MASE":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "average_MASE_real_world.csv"),
            # index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "rel_to_no_scaler_average_MASE_real_world.csv"
        )
    if metric == "scaled_agg_MAE":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "scaled_agg_MAE_real_world.csv"),
            # index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "rel_to_no_scaler_scaled_agg_MAE_real_world.csv"
        )
    
    df_error_scaler = metric_df[~(metric_df["scaler"]=='None')]
    df_error_no_scaler = metric_df[(metric_df["scaler"]=='None')]

    df_error_scaler.loc[:, ["exp_id", "model_id"]] = df_error_scaler.loc[:, ["exp_id", "model_id"]].astype(str)
    df_error_scaler.set_index(
        ["exp_id", "model_id"], inplace=True
    )

    df_error_no_scaler.loc[:, ["exp_id", "model_id"]] = df_error_no_scaler.loc[:, ["exp_id", "model_id"]].astype(str)

    df_error_no_scaler.set_index(["exp_id", "model_id"], inplace=True)

    df_error_scaler.sort_index(inplace=True)
    df_error_no_scaler.sort_index(inplace=True)
    print(df_error_scaler)
    print(df_error_no_scaler)
          
    metric_df_rel_to_no_scaler = (
        df_error_no_scaler[["MAE", "RMSE"]]
        .subtract(df_error_scaler[["MAE", "RMSE"]])
        .div(df_error_no_scaler[["MAE", "RMSE"]])
    )
    
    metric_df_rel_to_no_scaler.reset_index(inplace=True)
    df_error_scaler.reset_index(inplace=True)
    metric_df_rel_to_no_scaler[["scaler", "scaling_level"]] = df_error_scaler[["scaler", "scaling_level"]]
    metric_df_rel_to_no_scaler.set_index(["exp_id", "scaler", "scaling_level", "model_id"], inplace=True)
    # Write to a csv file
    metric_df_rel_to_no_scaler.to_csv(file_name_csv)



def postprocess_results_indi_both_df(original_df):
    df = original_df.copy()
    df = df[df["ID"] != "ALL"]
    # df.loc[:, "ID"] = df["ID"].astype(int)
    df_filtered = df[
        ["exp_id", "ID", "MAE", "RMSE", "type", "level", "model_id"]
    ]
    return df_filtered


def add_missing_cols(df):
    # Filter rows where 'type' == 'None' and 'level' == 'None'
    filtered_df = df[(df['type'] == 'None') & (df['level'] == 'None')]

    # Define new rows
    new_rows = [
        {'type': 'revin', 'level': 'batch', 'model_id': 'Naive'},
        {'type': 'revin', 'level': 'instance', 'model_id': 'Naive'},
    ]

    # Iterate over the filtered DataFrame
    for _, row in filtered_df.iterrows():
        # Create new rows based on the existing row and the new information
        for new_row_info in new_rows:
            new_row = row.copy()
            new_row.update(pd.Series(new_row_info))
            df = df.append(new_row, ignore_index=True)
    return df

def calculate_average_MASE_both():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    results_indi_merged = pd.read_csv(
        os.path.join(tables_dir, "results_indi_real_world_both.csv")
    )
    file_name_csv = os.path.join(tables_dir, "average_MASE_real_world_both.csv")

    df_error = results_indi_merged[
        ~results_indi_merged["model_id"].isin(["Naive", "SNaive"])
    ]
    df_ideal_error = results_indi_merged[results_indi_merged["model_id"] == "Naive"]


    # Filter rows in ideal_metrics_sampled where the multi-index matches
    filtered_df_ideal_error = add_missing_cols(df_ideal_error) 
    # print(filtered_df_ideal_error)
    df_error = postprocess_results_indi_both_df(df_error)
    filtered_df_ideal_error = postprocess_results_indi_both_df(filtered_df_ideal_error)

    filtered_df_ideal_error[
        ["ID", "exp_id", "type", "level"]
    ] = filtered_df_ideal_error[["ID", "exp_id", "type", "level"]].astype(str)
    filtered_df_ideal_error.set_index(
        ["ID", "exp_id", "type", "level"], inplace=True
    )

    df_error[["ID", "exp_id", "type", "level"]] = df_error[
        ["ID", "exp_id", "type", "level"]
    ].astype(str)
    df_error.set_index(["ID", "exp_id", "type", "level"], inplace=True)

    filtered_df_ideal_error.sort_index(inplace=True)
    df_error.sort_index(inplace=True)
    
    

    # Create a new DataFrame for division operation
    div_result = (
        df_error[["MAE", "RMSE"]]
        .div(filtered_df_ideal_error[["MAE", "RMSE"]])
    )
    div_result.reset_index(inplace=True)
    df_error.reset_index(inplace=True)
    

    # Concat other columns from df_error
    average_MASE_per_ID = pd.concat([div_result, df_error[["model_id"]]], axis=1)
    # average_MASE = average_MASE_per_ID
    average_MASE = average_MASE_per_ID.groupby(
        ["exp_id","type", "level", "model_id" ]
    ).mean()
    average_MASE.to_csv(file_name_csv)


def calculate_scaled_agg_MAE_both():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")
    results_indi_merged = pd.read_csv(
        os.path.join(tables_dir, "results_indi_real_world_both.csv")
    )
    file_name_csv = os.path.join(tables_dir, "scaled_agg_MAE_real_world_both.csv")
    df_error = results_indi_merged[
        ~results_indi_merged["model_id"].isin(["Naive", "SNaive"])
    ]
    df_ideal_error = results_indi_merged[results_indi_merged["model_id"] == "Naive"]

    filtered_df_ideal_error = add_missing_cols(df_ideal_error) 
    # print(filtered_df_ideal_error)
    df_error = postprocess_results_indi_both_df(df_error)
    filtered_df_ideal_error = postprocess_results_indi_both_df(filtered_df_ideal_error)

    filtered_df_ideal_error[
        ["ID", "exp_id", "scaler", "scaling_level"]
    ] = filtered_df_ideal_error[["ID", "exp_id", "type", "level"]].astype(str)
    filtered_df_ideal_error.set_index(
        ["ID", "exp_id", "type", "level"], inplace=True
    )

    df_error[["ID", "exp_id", "type", "level"]] = df_error[
        ["ID", "exp_id", "type", "level"]
    ].astype(str)
    df_error.set_index(["ID", "exp_id", "type", "level"], inplace=True)

    filtered_df_ideal_error.sort_index(inplace=True)
    df_error.sort_index(inplace=True)
    filtered_df_ideal_error.reset_index(inplace=True)
    df_error.reset_index(inplace=True)

    # create both avg errors
    filtered_df_ideal_error_mean = filtered_df_ideal_error.groupby(
        ["exp_id","type", "level", "model_id" ]
    ).mean()
    df_error_mean = df_error.groupby(
        ["exp_id","type", "level", "model_id" ]
    ).mean()

    filtered_df_ideal_error_mean.reset_index(level=3, inplace=True)
    df_error_mean.reset_index(level=3, inplace=True)

    # Create a new DataFrame for division operation
    div_result = (
        df_error_mean[["MAE", "RMSE"]]
        .div(filtered_df_ideal_error_mean[["MAE", "RMSE"]])
    )
    div_result.reset_index(inplace=True)
    df_error_mean.reset_index(inplace=True)

    # Concat other columns from df_error
    scaled_agg_MAE = pd.concat([div_result, df_error_mean[["model_id"]]], axis=1)
    
    scaled_agg_MAE.set_index(["exp_id"], inplace=True)
    scaled_agg_MAE.to_csv(file_name_csv)


def calculate_all_rel_to_no_scaler_for_metric(metric):
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    tables_dir = os.path.join(parent_dir, "tables")

    if metric == "average_MASE":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "average_MASE_real_world_both.csv"),
            # index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "average_MASE_rel_to_no_real_world_both.csv"
        )
    if metric == "scaled_agg_MAE":
        metric_df = pd.read_csv(
            os.path.join(tables_dir, "scaled_agg_MAE_real_world_both.csv"),
            # index_col=["exp_id"],
        )
        file_name_csv = os.path.join(
            tables_dir, "scaled_agg_MAE_rel_to_no_real_world_both.csv"
        )

    df_error_scaler = metric_df[~(metric_df["type"]=='None')]
    df_error_no_scaler = metric_df[(metric_df["type"]=='None')]
   
    df_error_scaler.loc[:, ["exp_id", "model_id"]] = df_error_scaler.loc[:, ["exp_id", "model_id"]].astype(str)
    df_error_scaler.set_index(
        ["exp_id", "model_id"], inplace=True
    )

    df_error_no_scaler.loc[:, ["exp_id", "model_id"]] = df_error_no_scaler.loc[:, ["exp_id", "model_id"]].astype(str)

    df_error_no_scaler.set_index(["exp_id", "model_id"], inplace=True)

    df_error_scaler.sort_index(inplace=True)
    df_error_no_scaler.sort_index(inplace=True)
    print(df_error_scaler)
    print(df_error_no_scaler)
          
    metric_df_rel_to_no_scaler = (
        df_error_no_scaler[["MAE", "RMSE"]]
        .subtract(df_error_scaler[["MAE", "RMSE"]])
        .div(df_error_no_scaler[["MAE", "RMSE"]])
    )
    
    metric_df_rel_to_no_scaler.reset_index(inplace=True)
    df_error_scaler.reset_index(inplace=True)
    metric_df_rel_to_no_scaler[["type", "level"]] = df_error_scaler[["type", "level"]]
    metric_df_rel_to_no_scaler.set_index(["exp_id", "type", "level", "model_id"], inplace=True)
    # Write to a csv file
    metric_df_rel_to_no_scaler.to_csv(file_name_csv)