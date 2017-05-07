from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def root():
    start = request.args.get('start')
    end = request.args.get('end')
    data = {
        'attempts': 'too many',
        'start':start,
        'end':end
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp

if __name__ == "__main__":
    app.run()