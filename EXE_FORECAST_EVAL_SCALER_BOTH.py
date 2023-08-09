from evaluation.forecast_scaler_both.merge_results import (
    merge_average_MASE, merge_scaled_agg_MAE)
from evaluation.forecast_scaler_both.process_scalers import (
    calculate_all_rel_to_no_scaler_for_metric,
    calculate_best_scaler_rel_to_no_scaler_for_metric,
    calculate_best_scalers_both, calculate_best_scalers_combined)
from evaluation.forecast_scaler_both.view_scaler import (
    create_boxplot_by_het_type, create_boxplot_by_model_id,
    create_faceted_box_plots, plot_bar_plots_best_scaler_rel_to_no,
    view_best_scaler_rel_to_no_scaler_for_metric_per_model_and_het_type,
    create_grouped_box_plots_per_norm_type,
    create_grouped_box_plots_per_norm_type_indi,
    create_boxplot_aggregated,
    create_grouped_box_plots_compare_level,

)
from evaluation.forecast_scaler_both.statistics import calculate_all_statistics, calculate_het_type_statistics, calculate_model_statistics

if __name__ == "__main__":
    # calculate_best_scalers_both("average_MASE")
    # calculate_best_scalers_both("scaled_agg_MAE")
    # calculate_best_scalers_combined("average_MASE")
    # calculate_best_scalers_combined("scaled_agg_MAE")
    # calculate_best_scaler_rel_to_no_scaler_for_metric("average_MASE", "combined")
    # calculate_best_scaler_rel_to_no_scaler_for_metric("scaled_agg_MAE", "combined")
    # view_best_scaler_rel_to_no_scaler_for_metric_per_model_and_het_type("average_MASE")
    # view_best_scaler_rel_to_no_scaler_for_metric_per_model_and_het_type("scaled_agg_MAE")
    # plot_bar_plots_best_scaler_rel_to_no("average_MASE", "MAE")
    # plot_bar_plots_best_scaler_rel_to_no("scaled_agg_MAE", "MAE")
    # merge_average_MASE()
    # merge_scaled_agg_MAE()
    # calculate_all_rel_to_no_scaler_for_metric("average_MASE")
    # calculate_all_rel_to_no_scaler_for_metric("scaled_agg_MAE")
    # create_faceted_box_plots("average_MASE", selected_norm_level=['per_time_series', 'instance'], selected_norm_type=["PowerTransformer", "LogTransformer", "QuantileTransformeroutput_distribution='normal'"])
    # create_boxplot_by_het_type("average_MASE", selected_norm_level=['per_time_series', 'instance'])
    # create_boxplot_by_model_id("average_MASE", selected_norm_level=['per_time_series', 'instance'])
    # create_faceted_box_plots("average_MASE")
    # create_boxplot_by_het_type("average_MASE")
    # create_boxplot_by_model_id("average_MASE")
    # create_faceted_box_plots("scaled_agg_MAE")
    # create_boxplot_by_het_type("scaled_agg_MAE")
    # create_boxplot_by_model_id("scaled_agg_MAE")
    # create_grouped_box_plots_per_norm_type("average_MASE")
    # create_grouped_box_plots_per_norm_type_indi("average_MASE")
    # calculate_all_statistics("average_MASE", selected_norm_level=['per_time_series', 'instance'])
    # calculate_all_statistics("average_MASE", selected_norm_level=['per_dataset', 'batch'])
    # calculate_het_type_statistics("average_MASE")
    # calculate_model_statistics("average_MASE")
    # calculate_all_statistics("scaled_agg_MAE")
    # create_boxplot_aggregated("average_MASE")
    create_grouped_box_plots_compare_level("average_MASE")