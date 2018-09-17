'''Default configuration settings for SKOPE services.'''
import sys

if 'pytest' not in sys.modules:
    TIMESERIES_SERVICE_BASE = '/timeseries-service/api/v1'
else:
    TIMESERIES_SERVICE_BASE = ''

TIMESERIES_SERVICE_NAME	= 'SKOPE Timeseries Service'
TIMESERIES_DATA_PATH_TEMPLATE = '../data/{datasetId}_{variableName}'
TIMESERIES_UNCERTAINTY_PATH_TEMPLATE = '../data/{datasetId}_{variableName}_uncertainty'
TIMESERIES_DATA_FILE_EXTENSIONS = ['.tif', '.nc', '.nc4']
TIMESERIES_GDALLOCATIONINFO_COMMAND = 'gdallocationinfo'
TIMESERIES_ZONALINFO_COMMAND = 'python ../../geoserver-loader/scripts/zonalinfo.py'
TIMESERIES_MAX_PROCESSING_TIME = 5000
