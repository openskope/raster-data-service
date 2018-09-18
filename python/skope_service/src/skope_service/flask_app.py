'''Define endpoints for timeseries service.'''

from flask import Flask, jsonify, request

from skope import RasterDataset

# create the Flask application instance
app = Flask(__name__)  # pylint: disable=invalid-name

# configure the Flask application with the default settings
app.config.from_object('skope_service.default_settings')

# extract the service base URI path from the configuration
SERVICE_BASE = app.config['TIMESERIES_SERVICE_BASE']

@app.route(SERVICE_BASE + '/status')
def get_status():
    '''Return the name and status of the timeseries service.'''
    return jsonify({'name': app.config['TIMESERIES_SERVICE_NAME']})

@app.route(SERVICE_BASE + '/timeseries/<dataset_id>/<variable_name>')
def get_timeseries(dataset_id, variable_name):
    '''Return the timeseries at specified point.'''

    longitude = float(request.args.get('longitude'))
    latitude = float(request.args.get('latitude'))
    start = request.args.get('start')
    end = request.args.get('end')

    raster_dataset = RasterDataset(
        'data/' + dataset_id + '_' + variable_name + '.tif')

    begin = None if start is None else int(start)
    end = None if end is None else int(end) + 1
    series = list(raster_dataset.series_at_point(longitude, latitude, begin, end))

    response_body = {
        'datasetId': dataset_id,
        'variableName': variable_name,
        'boundaryGeometry': {
            'type': 'Point',
            'coordinates': [longitude, latitude]
        },
        'start': '0' if begin is None else str(begin),
        'end': '4' if end is None else str(end-1),
        'values': series
    }

    return jsonify(response_body)

if __name__ == '__main__':
    app.run(port=8001, debug=True)
