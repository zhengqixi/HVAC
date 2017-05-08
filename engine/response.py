from flask import Flask, request, jsonify, redirect
import powerdash_info
import analytics
import get_clean_data

app = Flask(__name__)


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
        raise InvalidUsage('Please provide both the start and end times')
    if not start.isdigit() or not end.isdigit():
        raise InvalidUsage('Improper date format, please give time in milliseconds from UTC Epoch',
                           payload={'start': start, 'end': end})
    start = int(start)
    end = int(end)
    if end < start:
        raise InvalidUsage('start must come before end', payload={'start': start, 'end': end})

    if query == 'total_usage':
        data = total_usage(start, end)
        resp = jsonify(data)
        resp.status_code = 200
        return resp
    if query == 'utility_comparison':
        data = utility_comparison(start, end)
        resp = jsonify(data)
        resp.status_code = 200
        return resp
    if query not in powerdash_info.distribution_boards:
        raise InvalidUsage('Requested distribution board does not exist', payload={'requested': query})
    data = distribution_board(query, start, end)
    resp = jsonify(data)
    resp.status_code = 200
    return data


@app.route('/night_day/<query>', methods=['GET'])
def night_day(query):
    start = request.args.get('start')
    end = request.args.get('end')
    if not start.isdigit() and not end.isdigit():
        raise InvalidUsage('Improper date format, please give time in milliseconds from Epoch',
                           payload={'start': start, 'end': end})
    start = int(start)
    end = int(end)
    if end < start:
        raise InvalidUsage('start must come before end', payload={'start': start, 'end': end})
    if query == 'total_usage':
        data = total_usage(start, end)
        resp = jsonify(data)
        resp.status_code = 200
        return resp
    if query == 'utility_comparison':
        data = utility_comparison(start, end)
        resp = jsonify(data)
        resp.status_code = 200
        return resp
    if query not in powerdash_info.distribution_boards:
        raise InvalidUsage('Requested distribution board does not exist', payload={'requested': query})
    data = distribution_board(query, start, end)
    resp = jsonify(data)
    resp.status_code = 200
    return data


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


def total_usage(start, end):
    boards = get_clean_data.get_distribution_boards(start, end)
    utilities = get_clean_data.get_overall(start, end)
    if boards is None or utilities is None:
        raise InvalidUsage('No data for selected start and end times',
                           payload={'start': start, 'end': end, 'query': 'total_usage'})
    return analytics.total_usage(boards, utilities)


def utility_comparison(start, end):
    boards = get_clean_data.get_distribution_boards(start, end)
    utilities = get_clean_data.get_overall(start, end)
    if boards is None or utilities is None:
        raise InvalidUsage('No data for selected start and end times',
                           payload={'start': start, 'end': end, 'query': 'utility_comparison'})
    return analytics.utility_comparison(boards, utilities)


def distribution_board(board, start, end):
    pass


# For debugging and testing only
# Absolutely do not use on server...
if __name__ == "__main__":
    app.run(debug=True)
