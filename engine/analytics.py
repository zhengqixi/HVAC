import statsmodels.api as sm
from powerdash_info import utility_metadata


def convert_to_kwh(data):
    return data.resample('60T', label='right', closed='right').sum() / 60


def night_day_usage(data, peak_start, peak_end):
    on_peak = data.between_time(start_time=peak_start, end_time=peak_end)
    off_peak = data[~data.isin(on_peak)]
    return on_peak, off_peak


# Here for reference purposes....
# def min_max_sum_mean(data):
#    daily_min = data.resample('1D', label='right', closed='right').min()
#    daily_max = data.resample('1D', label='right', closed='right').max()
#    daily_mean = data.resample('1D', label='right', closed='right').mean()
#    daily_sum = data.resample('1D', label='right', closed='right').sum()
#    absolute_min = data.min()[0]
#    absolute_max = data.max()[0]
#    absolute_sum = data.sum()[0]
#    absolute_mean = data.mean()[0]
#    return daily_min, daily_max, daily_sum, daily_mean, absolute_min, absolute_max, absolute_sum, absolute_mean


def decompose(data):
    res = sm.tsa.seasonal_decompose(data)
    return res.trend, res.seasonal, res.resid


def total_usage(boards, utilities):
    rollup = {}

    for board, series in boards.items():
        rollup[board] = convert_to_kwh(series)

    for utility, series in utilities.items():
        rollup[utility] = convert_to_kwh(series)

    for key, series in rollup.items():
        rollup[key] = series.sum()
    rollup['Total'] = rollup['Utility 2'] + rollup['Utility 1']
    utility1_sum = 0
    utility2_sum = 0
    for board in utility_metadata['Utility 1']:
        if board in rollup:
            utility1_sum = utility1_sum + rollup[board]

    for board in utility_metadata['Utility 2']:
        if board in rollup:
            utility2_sum = utility2_sum + rollup[board]

    rollup['Other-Utility1'] = utility1_sum
    rollup['Other-Utility2'] = utility2_sum
    return rollup


def utility_comparison(boards, utilities):
    rolled = total_usage(boards, utilities)
    utility_rolled = {'Utility 1': rolled['Utility 1'], 'Utility 2': rolled['Utility 2']}
    utility1_boards = []
    utility2_boards = []

    for board in utility_metadata['Utility 1']:
        if board in rolled:
            utility1_boards.append((board, rolled[board]))

    for board in utility_metadata['Utility 2']:
        if board in rolled:
            utility2_boards.append((board, rolled[board]))

    utility1_boards.sort(key=lambda x: x[1])
    utility2_boards.sort(key=lambda x: x[1])

    utility_rolled['Utility 1 ranking'] = utility1_boards
    utility_rolled['Utility 2 ranking'] = utility2_boards
    return utility_rolled


def distribution_board(board):
    kwh = convert_to_kwh(board).resample('1D', label='right', closed='right').sum()
    # trend, freq, noise = decompose(kwh)
    max = kwh.max()
    average = kwh.mean()
    min = kwh.min()
    return {'daily': kwh, 'max': max, 'mean': average, 'min': min}
