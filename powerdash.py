from io import StringIO
import datetime
import requests
import pandas as pd
import config


def get_data(start, end, dgm=None, variables=None):
    payload = {'start': start, 'end': end, 'dgm': dgm, 'variables': variables, 'format': 'csv'}
    data = requests.get(url=config.powerdash_base_url + "/range", params=payload)
    if data.text == "":
        print("No data...\n")
        return None
    csv_data = StringIO(data.text)
    csv = pd.read_csv(csv_data)
    csv.fillna(value=0, method=None, inplace=True)
    csv.set_index(pd.DatetimeIndex(csv['time']), inplace=True)
    return csv

def get_all_data(start, end, variables=None):
    print("Dates: \n")
    start_timestamp = start.timestamp()*1000
    end_timestamp = end.timestamp()*1000
    data = {}
    for key, value in config.powerdash_name_to_dgm.items():
        print("Obtaining data for: " + key + '\n')
        board_data = get_data(start=start_timestamp, end=end_timestamp, dgm=value, variables=variables)
        data[key] = board_data
    return data

def convert_to_kwh(data):
    return data.resample('60T', label='right').sum()/60

def night_day_usage(data):
    peak_start= datetime.time(hour=9)
    peak_end = datetime.time(hour=21)



if __name__ == "__main__":
    start = datetime.datetime(2015, 10, 1)
    end = datetime.datetime(2015, 10, 2)
    raw_kw = get_all_data(start=start, end=end)
    kwh = {}
    for key, value in raw_kw.items():
        kwh[key] = convert_to_kwh(value)
    kwh_average_night_day = {}
    kwh_total_night_day = {}
    for key, value in kwh.items():
        average, sum = night_day_usage(value)

