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

@app.route(APPLICATION_ROOT + '/timeseries/<dataset_id>/<variable_name>')
def get_timeseries(dataset_id, variable_name):
    response_body = {
        'datasetId': dataset_id,
        'variableName': variable_name,
        'boundaryGeometry': { 
            'type': 'Point',
            'coordinates': [-123,45]
        },
        'start': '0',
        'end': '4',
        'values': [100,200,300,400,500]
    }
    return jsonify(response_body)


if __name__ == '__main__':
    app.run(port=8001, debug=True)

