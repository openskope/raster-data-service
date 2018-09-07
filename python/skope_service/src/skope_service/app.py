from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/timeseries-service/api/v1'

@app.route('/status')
def get_status():
    return jsonify({'name': 'SKOPE Timeseries Service'})

if __name__ == '__main__':
    app.run(port=8001, debug=True)

