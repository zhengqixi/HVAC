from io import StringIO
import datetime
import requests
import pandas as pd
import powerdash_info
import statsmodels.api as sm


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
    csv.fillna(value=0, method=None, inplace=True)
    csv.set_index(pd.DatetimeIndex(csv['time']), inplace=True)
    del csv['time']
    return csv


def get_all_data(start, end):
    data = {}
    for key, value in powerdash_info.powerdash_name_to_dgm.items():
        print("Obtaining data for: " + key + '\n')
        board_data = get_data(start=start, end=end, board_name=key)
        data[key] = board_data
    return data


def convert_to_kwh(data):
    return data.resample('60T', label='right', closed='right').sum() / 60


def night_day_usage(data, peak_start, peak_end):
    peak_start = datetime.time(hour=9)
    peak_end = datetime.time(hour=21)
    on_peak = data.between_time(start_time=peak_start, end_time=peak_end)
    off_peak = data[~data.isin(on_peak)]
    return on_peak, off_peak


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

def decompose(data):
    res = sm.tsa.seasonal_decompose(data)
    return res.trend, res.seasonal, res.resid


if __name__ == "__main__":
    start = datetime.datetime(2015, 10, 1)
    end = datetime.datetime(2015, 11, 30)
    raw_kw = get_data(start=start, end=end, board_name= "sub-cellar power and lighting")
    peak_start = datetime.time(9)
    peak_end = datetime.time(21)
    kwh = convert_to_kwh(raw_kw)
    on_peak, off_peak = night_day_usage(kwh, peak_start, peak_end)
    on_peak_average, _, _, _, _, _, _, _ = min_max_sum_mean(on_peak)
    off_peak_average, _, _, _, _, _, _, _ = min_max_sum_mean(off_peak)
    on_trend, on_seasonal, on_noise = decompose(on_peak_average)
    off_trend, off_seasonal, off_noise = decompose(off_peak_average)
    print(on_trend)
    print(off_trend)
    print(on_seasonal)
    print(off_seasonal)



