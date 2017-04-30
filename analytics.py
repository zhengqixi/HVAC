from io import StringIO
import datetime
import requests
import pandas as pd
import powerdash_info


def get_data(start, end, dgm=None, variables=None):
    payload = {'start': start, 'end': end, 'dgm': dgm, 'variables': variables, 'format': 'csv'}
    data = requests.get(url=powerdash_info.powerdash_base_url + "/range", params=payload)
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
    for key, value in powerdash_info.powerdash_name_to_dgm.items():
        print("Obtaining data for: " + key + '\n')
        board_data = get_data(start=start_timestamp, end=end_timestamp, dgm=value, variables=variables)
        data[key] = board_data
    return data

def convert_to_kwh(data):
    return data.resample('60T', label='right', closed='right').sum()/60

def night_day_usage(data, peak_start, peak_end):
    peak_start= datetime.time(hour=9)
    peak_end = datetime.time(hour=21)
    on_peak = data.between_time(start_time=peak_start, end_time=peak_end)
    off_peak = data[~data.isin(on_peak)]
    on_peak_total = on_peak.sum()[0]
    off_peak_total = off_peak.sum()[0]
    on_peak_daily= on_peak.resample('1D', label='right', closed='right').sum()
    off_peak_daily = off_peak.resample('1D', label='right', closed='right').sum()
    on_peak_mean = on_peak_daily.mean()[0]
    off_peak_mean = off_peak_daily.mean()[0]
    return on_peak_daily, on_peak_mean, on_peak_total, off_peak_daily, off_peak_mean, off_peak_total

def min_max_sum_mean(data):
    daily_min = data.resample('1D', label='right', closed='right').min()
    daily_max = data.resample('1D', label='right', closed='right').max()
    daily_mean = data.resample('1D', label='right', closed='right').mean()
    daily_sum = data.resample('1D', label='right', closed='right').sum()
    absolute_min = data.min()[0]
    absolute_max = data.max()[0]
    absolute_sum = data.sum()[0]
    absolute_mean = data.mean()[0]
    return daily_min, daily_max, daily_sum, daily_mean, absolute_min, absolute_max, absolute_sum, absolute_mean



if __name__ == "__main__":
    start = datetime.datetime(2015, 10, 1)
    end = datetime.datetime(2015, 11, 30)
    raw_kw = get_all_data(start=start, end=end)
    kwh = {}
    for key, value in raw_kw.items():
        kwh[key] = convert_to_kwh(value)
    kwh_mean_night = {}
    kwh_mean_day= {}
    peak_start= datetime.time(hour=9)
    peak_end = datetime.time(hour=21)
    for key, value in kwh.items():
        daily_min, daily_max, daily_sum, daily_mean, absolute_min, absolute_max, absolute_sum, absolute_mean = min_max_sum_mean(value)
        print(key + ':\n')
        print("Average: " + str(absolute_mean) + '\n')
        print("Total: " + str(absolute_sum) + '\n')
        print("Min: " + str(absolute_min) + '\n')
        print("Max: " + str(absolute_max) + '\n')
        print("Daily Average:\n")
        print(daily_mean)
        print('\n')
        print("Daily Sum:\n")
        print(daily_sum)
        print('\n')
        print("Daily Min:\n")
        print(daily_min)
        print('\n')
        print("Daily Max:\n")
        print(daily_max)
        print('\n')




