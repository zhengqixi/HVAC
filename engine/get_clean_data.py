from io import StringIO

import pandas as pd
import powerdash_info
import requests


def get_data(start, end, board_name=None):
    payload = {'start': start, 'end': end, 'dgm': powerdash_info.powerdash_name_to_dgm[board_name],
               'format': 'csv'}
    data = requests.get(url=powerdash_info.powerdash_base_url + "/range", params=payload)
    if data.text == "":
        return None
    csv_data = StringIO(data.text)
    csv = pd.read_csv(csv_data)
    csv.set_index(pd.DatetimeIndex(csv['time']), inplace=True)
    del csv['time']
    clean_data(csv)
    if board_name == "overall utilities":
        return csv
    return csv[powerdash_info.powerdash_name_to_series[board_name]]


def clean_data(data):
    data.fillna(value=0, method=None, inplace=True)


def get_distribution_boards(start, end):
    data = {}
    for board in powerdash_info.distribution_boards:
        board_data = get_data(start=start, end=end, board_name=board)
        if board_data is None:
            return None
        data[board] = board_data
    return data


def get_overall(start, end):
    overall = get_data(start=start, end=end, board_name="overall utilities")
    if overall is None:
        return None
    data = {}
    data['Utility 1'] = overall['SRV1KW']
    data['Utility 2'] = overall['SV2KW']
    return data


class cache_data:
    def __init__(self, start, end, board, data):
        self.start = start
        self.end = end
        self.board = board
        self.data = data


if __name__ == "__main__":
    start = 1448946000000
    end = 1449118800000
    data = get_overall(start=start, end=end)
    print(data)
