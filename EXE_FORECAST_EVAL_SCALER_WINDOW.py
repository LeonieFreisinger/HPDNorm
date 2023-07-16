from evaluation.forecast_scaler_window.merge_results import merge_results
from evaluation.forecast_scaler_window.process_scaler import (
    calculate_average_MASE, calculate_best_scaler_dif_to_no_scaler_for_metric,
    calculate_best_scaler_for_metric, calculate_scaled_agg_MAE)
from evaluation.forecast_scaler_window.view_scaler import (
    plot_bar_plots_best_scaler_dif_to_no,
    view_best_scaler_dif_to_no_scaler_for_metric_per_model_and_het_type)

if __name__ == "__main__":
    merge_results()
    calculate_average_MASE()
    calculate_best_scaler_for_metric("average_MASE")
    calculate_scaled_agg_MAE()
    calculate_best_scaler_for_metric("scaled_agg_MAE")
    calculate_best_scaler_dif_to_no_scaler_for_metric("scaled_agg_MAE")
    calculate_best_scaler_dif_to_no_scaler_for_metric("average_MASE")
    view_best_scaler_dif_to_no_scaler_for_metric_per_model_and_het_type(
        "scaled_agg_MAE", ["MAE"]
    )
    view_best_scaler_dif_to_no_scaler_for_metric_per_model_and_het_type(
        "scaled_agg_MAE", ["norm_type", "norm_level", "learnable"]
    )
    view_best_scaler_dif_to_no_scaler_for_metric_per_model_and_het_type(
        "average_MASE", ["MAE"]
    )
    view_best_scaler_dif_to_no_scaler_for_metric_per_model_and_het_type(
        "average_MASE", ["norm_type", "norm_level", "learnable"]
    )
    plot_bar_plots_best_scaler_dif_to_no("scaled_agg_MAE", "MAE")
    plot_bar_plots_best_scaler_dif_to_no("average_MASE", "MAE")
