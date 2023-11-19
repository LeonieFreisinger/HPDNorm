import os
import random
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tot.error_utils import raise_if

DATA_DIR = os.path.join(Path(__file__).parent.parent.parent.absolute(), "datasets")


def conditional_download(file_id, destination):
    if not os.path.exists(destination):
        print(f"Downloading dataset to {destination}...")
        download_file_from_google_drive(file_id, destination)


def download_file_from_google_drive(id, destination):
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={"id": id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    # In case we do not get a token in the cookies, we try to extract it from the page content
    soup = BeautifulSoup(response.text, "html.parser")
    tag = soup.find("a", id="uc-download-link")
    if tag:
        return tag["href"].split("confirm=")[1].split("&")[0]

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


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
    file_id = "1i36JO5HWltxBMB0AVg2p8q31XuiSVHcP"
    destination = DATA_DIR + "/eia_electricity_hourly.csv"
    conditional_download(file_id, destination)

    return load(
        destination,
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
    file_id = "1pNpVXovDHIiA__bxym4vpcHFwSb9VFv7"
    destination = DATA_DIR + "/london_electricity_hourly.csv"
    conditional_download(file_id, destination)

    return load(
        destination,
        ids=["T1", "T33", "T67", "T89", "T122", "T156", "T180", "T209", "T281", "T307"],
        n_samples=26280,
    )


def load_ERCOT():
    file_id = "1c8QZhcSoGA1jvcWajChsr1cFvnBJk"
    destination = DATA_DIR + "/ercot_load_reduced.csv"
    conditional_download(file_id, destination)

    return load(destination)


def load_Australian():
    file_id = "1GouZJ97OgsiWn5LOQtJSd51RiDL9_fwm"
    destination = DATA_DIR + "/australian_electricity_half_hourly.csv"
    conditional_download(file_id, destination)
    return load(destination, n_ids=5, n_samples=52560)


def load_Solar():
    file_id = "1tCHJQy7KdQSlr6xhqHwBZogWiCn6nERL"
    destination = DATA_DIR + "/solar_10_minutes_dataset.csv"
    conditional_download(file_id, destination)

    return load(
        destination,
        ids=["T1", "T19", "T34", "T59", "T66", "T83", "T91", "T111", "T124", "T134"],
        n_samples=26280,
    )


def load_ETTh():
    file_id = "1CfZPuHSZOSwYgA7tkMNi2FIVbCDWhu2B"
    destination = DATA_DIR + "/ETTh_panel.csv"
    conditional_download(file_id, destination)

    return load(destination, n_ids=14, n_samples=26280)


def load_WebTraffic():
    file_id = "1Pq18u43zRDfb6dVSnnWhEOalAWzgy_Mt"
    destination = DATA_DIR + "/kaggle_web_traffic_1000.csv"
    conditional_download(file_id, destination)

    return load(destination)


def load_M5():
    file_id = "1H2LR4_lvmFsT_HFaYeyOuJ2AiEVj69RH"
    destination = DATA_DIR + "/m5_aggregated_3049.csv"
    conditional_download(file_id, destination)

    return load(destination)


DATASETS = {
    "EIA": {"load": load_EIA, "freq": "H"},
    "London": {"load": load_London, "freq": "H"},
    "ERCOT": {"load": load_ERCOT, "freq": "H"},
    "Australian": {"load": load_Australian, "freq": "30min"},
    "Solar": {"load": load_Solar, "freq": "10min"},
    "ETTh": {"load": load_ETTh, "freq": "H"},
    "WebTraffic": {"load": load_WebTraffic, "freq": "D"},
    "M5": {"load": load_M5, "freq": "D"},
}
