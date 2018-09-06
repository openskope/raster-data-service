from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def get_status():
    return jsonify({'name': 'SKOPE Timeseries Service'})

if __name__ == '__main__':
    app.run(port=8001, debug=True)

