from flask import Flask, request, jsonify, redirect
import powerdash_info
import analytics
import get_clean_data

app = Flask(__name__)


@app.route('/standard/<query>', methods=['GET'])
def standard(query):
    start = request.args.get('start')
    end = request.args.get('end')
    data = {
        'start': start,
        'end': end,
        'request': distribution_board
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@app.route('/night_day/<query>', methods=['GET'])
def night_day(query):
    start = request.args.get('start')
    end = request.args.get('end')
    peak_start = request.args.get('peak_start')
    peak_end = request.args.get('peak_end')


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
    pass
def utility_comparison(start, end):
    pass
def distribution_board(board, start, end):
    pass

# For debugging and testing only
# Absolutely do not use on server...
if __name__ == "__main__":
    app.run(debug=True)
