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
    del csv['time']
    return csv

def get_all_data(start, end, variables=None):
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
    on_peak = data.between_time(start_time=peak_start, end_time=peak_end)
    off_peak = data[~data.isin(on_peak)]
    on_peak_total = on_peak.sum()[0]
    off_peak_total = off_peak.sum()[0]
    on_peak_daily= on_peak.groupby(on_peak.index.year, on_peak.index.month, on_peak.index.day).sum()
    off_peak_daily = off_peak.groupby(on_peak.index.year, off_peak.index.month, off_peak.index.day).sum()
    on_peak_average = on_peak_daily.mean()[0]
    off_peak_average = off_peak_daily.mean()[0]
    return on_peak_daily, on_peak_average, on_peak_total, off_peak_daily, off_peak_average, off_peak_total



if __name__ == "__main__":
    start = datetime.datetime(2015, 10, 10)
    end = datetime.datetime(2015, 11, 10)
    raw_kw = get_all_data(start=start, end=end)
    kwh = {}
    for key, value in raw_kw.items():
        kwh[key] = convert_to_kwh(value)
    kwh_average_night = {}
    kwh_total_night = {}
    kwh_average_day= {}
    kwh_total_day= {}
    #for key, value in kwh.items():

