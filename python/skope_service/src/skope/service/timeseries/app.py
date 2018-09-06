from flask import jsonify, request
from settings import app

@app.route('/timeseries-service/api/v1/status')
def get_status():
    return jsonify({'name': 'SKOPE Timeseries Service'})

if __name__ == '__main__':
    app.run(port=8001, debug=True)

