import datetime
import statsmodels.api as sm


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
