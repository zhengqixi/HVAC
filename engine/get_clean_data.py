import powerdash_info
import requests
from io import StringIO
import pandas as pd


def get_data(start, end, board_name=None):
    start_timestamp = start.timestamp() * 1000
    end_timestamp = end.timestamp() * 1000
    payload = {'start': start_timestamp, 'end': end_timestamp, 'dgm': powerdash_info.powerdash_name_to_dgm[board_name],
               'format': 'csv'}
    data = requests.get(url=powerdash_info.powerdash_base_url + "/range", params=payload)
    if data.text == "":
        print("No data...\n")
        return None
    csv_data = StringIO(data.text)
    csv = pd.read_csv(csv_data)
    csv.set_index(pd.DatetimeIndex(csv['time']), inplace=True)
    del csv['time']
    clean_data(csv)
    return csv


def get_all_data(start, end):
    data = {}
    for key, value in powerdash_info.powerdash_name_to_dgm.items():
        print("Obtaining data for: " + key + '\n')
        board_data = get_data(start=start, end=end, board_name=key)
        data[key] = board_data
    clean_all_data(data)
    return data


def clean_data(data):
    data.fillna(value=0, method=None, inplace=True)

def clean_all_data(data):
    pass
