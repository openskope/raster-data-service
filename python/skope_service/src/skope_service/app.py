import sys
from flask import Flask, jsonify, request

app = Flask(__name__)

if 'pytest' not in sys.modules:
    APPLICATION_ROOT = '/timeseries-service/api/v1'
else:
    APPLICATION_ROOT = ''

@app.route(APPLICATION_ROOT + '/status')
def get_status():
    return jsonify({'name': 'SKOPE Timeseries Service'})

if __name__ == '__main__':
    app.run(port=8001, debug=True)

