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
        return None
    csv_data = StringIO(data.text)
    csv = pd.read_csv(csv_data)
    csv.set_index(pd.DatetimeIndex(csv['time']), inplace=True)
    del csv['time']
    clean_data(csv)
    return csv

def clean_data(data):
    data.fillna(value=0, method=None, inplace=True)

def get_distribution_boards(start, end):
    data = {}
    for board in powerdash_info.distribution_boards:
        board_data = get_data(start=start, end=end, board_name=board)
        data[board] = board_data[powerdash_info.powerdash_name_to_series[board]]
    return data

def get_overall(start, end):
    overall = get_data(start=start, end=end, board_name="overall utilities")
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
    import datetime
    start = datetime.datetime(year=2015, month=12, day=1)
    end = datetime.datetime(year=2015, month=12, day=3)
    data = get_distribution_boards(start=start, end=end)
    print(data)
