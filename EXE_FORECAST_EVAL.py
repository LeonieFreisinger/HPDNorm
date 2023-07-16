from evaluation.forecast_no_scaler.merge_results import merge_results
from evaluation.forecast_no_scaler.process_no_scaler import (
    calculate_average_MASE, calculate_scaled_aggregate_MAE,
    find_first_exceeding_threshold, plot_sampled_error)

if __name__ == "__main__":
    # merge_results()
    # calculate_scaled_aggregate_MAE()
    # calculate_average_MASE()
    plot_sampled_error()
    find_first_exceeding_threshold()
