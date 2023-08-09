from evaluation.forecast_real_world.merge_results import merge_results, merge_results_wb, merge_both
from evaluation.forecast_real_world.process_scaler import \
calculate_scaled_agg_MAE, calculate_average_MASE, calculate_error_rel_to_no_scaler_for_metric,\
      calculate_average_MASE_both,calculate_scaled_agg_MAE_both, calculate_all_rel_to_no_scaler_for_metric
from evaluation.forecast_real_world.view_scaler import create_faceted_box_plots, create_boxplot_by_model_id,\
create_boxplot_by_dataset, create_grouped_box_plots_per_norm_type, create_grouped_box_plots_per_norm_type_indi,\
create_boxplot_aggregated
from evaluation.forecast_real_world.statistics import calculate_dataset_statistics, calculate_model_statistics,\
calculate_all_statistics

if __name__ == "__main__":
    # merge_results()
    # merge_results_wb()
    # merge_both()
    # calculate_scaled_agg_MAE()
    # calculate_average_MASE()
    # calculate_average_MASE_both()
    # calculate_scaled_agg_MAE_both()
    # calculate_error_rel_to_no_scaler_for_metric("average_MASE")
    # calculate_error_rel_to_no_scaler_for_metric("scaled_agg_MAE")
    # calculate_all_rel_to_no_scaler_for_metric("average_MASE")
    # calculate_all_rel_to_no_scaler_for_metric("scaled_agg_MAE")
    # create_faceted_box_plots("average_MASE")
    # create_faceted_box_plots(
    #     "average_MASE", 
    #     selected_norm_level=["per_time_series"],
    #     selected_norm_type = ["RobustScaler", "StandardScaler"]
    # )
    # create_faceted_box_plots("average_MASE", selected_norm_level=["per_dataset"],)
    # create_faceted_box_plots("scaled_agg_MAE")
    # create_boxplot_by_model_id("average_MASE")
    # create_boxplot_by_dataset("average_MASE")
    # create_faceted_box_plots("scaled_agg_MAE")
    # create_boxplot_by_model_id("scaled_agg_MAE")
    # create_boxplot_by_dataset("scaled_agg_MAE")
    # create_grouped_box_plots_per_norm_type("average_MASE")
    # create_grouped_box_plots_per_norm_type_indi("average_MASE")
    
    # calculate_dataset_statistics("average_MASE", selected_norm_level=['per_time_series', 'instance'])
    # calculate_dataset_statistics("average_MASE", selected_norm_level=['per_dataset', 'batch'])
    # calculate_model_statistics("average_MASE", selected_norm_level=['per_dataset', 'batch'])
    # calculate_model_statistics("average_MASE", selected_norm_level=['per_time_series', 'instance'])
    # calculate_all_statistics("average_MASE", selected_norm_level=['per_dataset', 'batch'])
#     calculate_all_statistics("average_MASE", selected_norm_level=['per_time_series', 'instance'])
    # calculate_all_statistics("scaled_agg_MAE")
    # calculate_all_statistics("average_MASE")
    # calculate_model_statistics("average_MASE")
    # calculate_dataset_statistics("average_MASE")
    create_boxplot_aggregated("average_MASE")