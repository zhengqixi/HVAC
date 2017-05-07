from flask import Flask, request, jsonify, redirect
import powerdash_info
app = Flask(__name__)


@app.route('/standard/<distribution_board>', methods = ['GET'])
def standard(distribution_board):
    start = request.args.get('start')
    end = request.args.get('end')
    data = {
        'board': distribution_board,
        'start':start,
        'end':end
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/night_day/<distribution_board>', methods = ['GET'])
def night_day(distribution_board):
    start = request.args.get('start')
    end = request.args.get('end')
    peak_start = request.args.get('peak_start')
    peak_end = request.args.get('peak_end')
    data = {
        'board': distribution_board,
        'start':start,
        'end':end
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route('/metadata', methods = ['GET'])
def metadata():
    resp = jsonify(powerdash_info.floor_metadata)
    resp.status_code = 200
    return resp



if __name__ == "__main__":
    app.run()