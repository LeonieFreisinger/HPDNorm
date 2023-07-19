import os
import random
from pathlib import Path

import pandas as pd
from tot.error_utils import raise_if

print(Path(__file__).parent.parent.parent.absolute())
DATA_DIR = os.path.join(Path(__file__).parent.parent.parent.absolute(), "datasets")


def load(path, n_samples=None, ids=None, n_ids=None):
    df = pd.read_csv(path)

    raise_if(
        ids is not None and n_ids is not None,
        "Remove specified ids from input if you want to select a number of ids.",
    )
    if ids is None and n_ids is not None:
        unique_ids = df["ID"].unique()
        ids = random.sample(list(unique_ids), k=n_ids)

    if ids is not None:
        df = df[df["ID"].isin(ids)].reset_index(drop=True)
    if n_samples is not None:
        df = (
            df.groupby("ID")
            .apply(lambda x: x.iloc[:n_samples, :].copy(deep=True))
            .reset_index(drop=True)
        )
    return df


def load_EIA():
    return load(
        DATA_DIR + "/eia_electricity_hourly.csv",
        ids=[
            "AEC",
            "AECI",
            "AVA",
            "AZPS",
            "BANC",
            "BPAT",
            "CHPD",
            "CISO",
            "CPLE",
            "CPLW",
        ],
        n_samples=26280,
    )


def load_London():
    return load(
        DATA_DIR + "/london_electricity_hourly.csv",
        ids=["T1", "T33", "T67", "T89", "T122", "T156", "T180", "T209", "T281", "T307"],
        n_samples=26280,
    )


def load_ERCOT():
    return load(DATA_DIR + "/ercot_load_reduced.csv")


def load_Australian():
    return load(
        DATA_DIR + "/australian_electricity_half_hourly.csv", n_ids=5, n_samples=52560
    )


def load_Solar():
    return load(
        DATA_DIR + "/solar_10_minutes_dataset.csv",
        ids=["T1", "T19", "T34", "T59", "T66", "T83", "T91", "T111", "T124", "T134"],
        n_samples=26280,
    )


def load_ETTh():
    return load(DATA_DIR + "/ETTh_panel.csv", n_ids=14, n_samples=26280)


DATASETS = {
    "EIA": {"load": load_EIA, "freq": "H"},
    "London": {"load": load_London, "freq": "H"},
    "ERCOT": {"load": load_ERCOT, "freq": "H"},
    "Australian": {"load": load_Australian, "freq": "30min"},
    "Solar": {"load": load_Solar, "freq": "10min"},
    "ETTh": {"load": load_ETTh, "freq": "H"},
}
