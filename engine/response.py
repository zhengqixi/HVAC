import datetime
import time

import analytics
import get_clean_data
import powerdash_info
import redis
from flask import Flask, request, jsonify

app = Flask(__name__)
db = redis.Redis('localhost')


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/standard/<query>', methods=['GET'])
def standard(query):
    start = request.args.get('start')
    end = request.args.get('end')
    # error handling
    if start is None or end is None:
        raise InvalidUsage('Please provide both the start and end times', payload={'start': start, 'end': end})
    if not start.isdigit() or not end.isdigit():
        raise InvalidUsage('Improper date format, please give time in milliseconds from UTC Epoch',
                           payload={'start': start, 'end': end})

    start = int(start)
    end = int(end)
    if end < start:
        raise InvalidUsage('start must come before end', payload={'start': start, 'end': end})

    if query == 'total_usage' or query == 'utility_comparison':
        boards = get_clean_data.get_distribution_boards(start, end, db)
        utilities = get_clean_data.get_overall(start, end, db)
        if boards is None or utilities is None:
            raise InvalidUsage('No data for selected start and end times',
                               payload={'start': start, 'end': end, 'query': 'total_usage'})
        data = ''
        if query == 'total_usage':
            data = analytics.total_usage(boards, utilities)
        elif query == 'utility_comparison':
            data = analytics.utility_comparison(boards, utilities)
        resp = jsonify(data)
        resp.status_code = 200
        return resp

    if query not in powerdash_info.distribution_boards:
        raise InvalidUsage('Requested distribution board does not exist', payload={'requested': query})

    board_data = get_clean_data.get_data(start, end, query, db)
    if board_data is None:
        raise InvalidUsage('No data for selected start and end times',
                           payload={'start': start, 'end': end, 'query': query})
    data = analytics.distribution_board(board_data)
    data['time'] = data['daily'].index.values.tolist()
    data['daily'] = data['daily'].tolist()
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@app.route('/night_day/<query>', methods=['GET'])
def night_day(query):
    start = request.args.get('start')
    end = request.args.get('end')
    peak_start = request.args.get('peak_start')
    peak_end = request.args.get('peak_end')
    # error handling
    if start is None or end is None:
        raise InvalidUsage('Please provide both the start and end times', payload={'start': start, 'end': end})
    if not start.isdigit() or not end.isdigit():
        raise InvalidUsage('Improper date format, please give time in milliseconds from UTC Epoch',
                           payload={'start': start, 'end': end})
    if peak_start is None or peak_end is None:
        raise InvalidUsage('Please provide both the start and end times for the peak time',
                           payload={'start': peak_start, 'end': peak_end})
    try:
        peak_start = time.strptime(peak_start, '%H:%M')
    except ValueError:
        raise InvalidUsage('Invalid time format', payload={'peak_start': peak_start})
    try:
        peak_end = time.strptime(peak_end, '%H:%M')
    except ValueError:
        raise InvalidUsage('Invalid time format', payload={'peak_start': peak_end})
    if start >= end:
        raise InvalidUsage('Peak start must be before peak end',
                           payload={'peak_start': peak_start, 'peak_end': peak_end})
    start = int(start)
    end = int(end)
    if end < start:
        raise InvalidUsage('start must come before end', payload={'start': start, 'end': end})

    peak_end = datetime.time(hour=peak_end.tm_hour, minute=peak_end.tm_sec)
    peak_start = datetime.time(hour=peak_start.tm_hour, minute=peak_start.tm_sec)

    if query == 'total_usage' or query == 'utility_comparison':
        boards = get_clean_data.get_distribution_boards(start, end, db)
        utilities = get_clean_data.get_overall(start, end, db)
        if boards is None or utilities is None:
            raise InvalidUsage('No data for selected start and end times',
                               payload={'start': start, 'end': end, 'query': 'total_usage'})
        data = {}
        boards_on_peak = {}
        boards_off_peak = {}
        utilities_on_peak = {}
        utilities_off_peak = {}
        for board, board_data in boards.items():
            on_peak, off_peak = analytics.night_day_usage(board_data, peak_start, peak_end)
            boards_on_peak[board] = on_peak
            boards_off_peak[board] = off_peak
        for utility, utility_data in utilities.items():
            on_peak, off_peak = analytics.night_day_usage(utility_data, peak_start, peak_end)
            utilities_on_peak[utility] = on_peak
            utilities_off_peak[utility] = off_peak

        if query == 'total_usage':
            data['on_peak'] = analytics.total_usage(boards_on_peak, utilities_on_peak)
            data['off_peak'] = analytics.total_usage(boards_off_peak, utilities_off_peak)
        elif query == 'utility_comparison':
            data['on_peak'] = analytics.utility_comparison(boards_on_peak, utilities_on_peak)
            data['off_peak'] = analytics.utility_comparison(boards_off_peak, utilities_off_peak)
        resp = jsonify(data)
        resp.status_code = 200
        return resp

    if query not in powerdash_info.distribution_boards:
        raise InvalidUsage('Requested distribution board does not exist', payload={'requested': query})

    board_data = get_clean_data.get_data(start, end, query, db)
    if board_data is None:
        raise InvalidUsage('No data for selected start and end times',
                           payload={'start': start, 'end': end, 'query': query})
    board_on, board_off = analytics.night_day_usage(board_data, peak_start, peak_end)
    data = {}
    on_peak_board = analytics.distribution_board(board_on)
    on_peak_board['time'] = on_peak_board['daily'].index.values.tolist()
    on_peak_board['daily'] = on_peak_board['daily'].tolist()
    off_peak_board = analytics.distribution_board(board_off)
    off_peak_board['time'] = off_peak_board['daily'].index.values.tolist()
    off_peak_board['daily'] = off_peak_board['daily'].tolist()
    data['on_peak'] = on_peak_board
    data['off_peak'] = off_peak_board
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@app.route('/metadata', methods=['GET'])
def metadata():
    metadata = {
        'distribution boards': powerdash_info.distribution_boards,
        'distribution_board_metadata': powerdash_info.distribution_board_metadata,
        'Utility metadata': powerdash_info.utility_metadata
    }
    resp = jsonify(metadata)
    resp.status_code = 200
    return resp


# For debugging and testing only
# Absolutely do not use on server...
if __name__ == "__main__":
    app.run(debug=True)
