import numpy as np


def calc_ar_series(ar_group, coeffs):
    ar_group_padded = np.pad(ar_group, (0, 4), mode="constant", constant_values=0)
    coeffs = np.flip(coeffs)
    # ar_group_predictions = np.apply_along_axis(lambda row: np.convolve(row, coeffs, mode='valid'), arr=ar_group_padded)
    ar_group_predictions = np.convolve(ar_group_padded, coeffs, mode="valid")

    return ar_group_predictions
