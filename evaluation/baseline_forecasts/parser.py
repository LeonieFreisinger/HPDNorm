import os
import pathlib
import re
from shutil import copyfile

import pandas as pd

pattern = r"(\w+)_n_ts_\[(.*?)\]_am_\[(.*?)\]_of_\[(.*?)\]_gr(?:_\[(.*?)\])?(?:_None_(.*?))?(?:_gr_([\[\],.\d]+))?$"


def extract_args_from_name(name):
    match = re.search(pattern, name)
    if match:
        data_func = match.group(1)
        n_ts_groups = list(map(int, match.group(2).split(", ")))
        amplitude_per_group = list(map(int, match.group(3).split(", ")))
        offset_per_group = list(map(int, match.group(4).split(", ")))
        data_trend_gradient_per_group = (
            list(map(float, match.group(5).split(", ")))
            if match.group(5)
            else match.group(5)
        )
        proportion_break = (
            list(map(int, match.group(6)[1:-1].split(", ")))
            if match.group(6)
            else match.group(6)
        )
        args = {
            "data_func": data_func,
            "n_ts_groups": n_ts_groups,
            "amplitude_per_group": amplitude_per_group,
            "offset_per_group": offset_per_group,
            "data_trend_gradient_per_group": data_trend_gradient_per_group,
            "proportion_break": proportion_break,
        }
    return args


def parse_synthetic_data_files():
    parent_dir = pathlib.Path(__file__).parent.parent.absolute()
    res_path = os.path.join(
        pathlib.Path(__file__).parent.parent.parent.absolute(), "results_no_scaler"
    )

    dfs_dict = {}

    for exp in os.listdir(res_path):
        exp_path = os.path.join(res_path, exp)
        if os.path.isdir(exp_path):
            results_csv_path = os.path.join(exp_path, "data.csv")
            if os.path.isfile(results_csv_path):

                # read csv
                df = pd.read_csv(results_csv_path)

                # round the number to 4 decimal places
                df = df.round(4)

                # append to the list
                dfs_dict[exp] = df

    return dfs_dict
