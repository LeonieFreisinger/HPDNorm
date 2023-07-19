from evaluation.forecast_real_world.merge_results import merge_results
from evaluation.forecast_real_world.process_scaler import \
    calculate_average_MASE

if __name__ == "__main__":
    merge_results()
    calculate_average_MASE()
