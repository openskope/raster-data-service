import numpy as np
import pytest
import skope.analysis

from osgeo import gdal

################################################################################
# Constants defined for this module.
################################################################################

DATASET_ROW_COUNT            = 2
DATASET_COLUMN_COUNT         = 2
DATASET_BAND_COUNT           = 2
DATASET_ORIGIN_LONGITUDE     = -123
DATASET_ORIGIN_LATITUDE      = 45
DATASET_PIXEL_SIZE_LONGITUDE = 1.0
DATASET_PIXEL_SIZE_LATITUDE  = 1.0
DATASET_NODATA_VALUE         = float('nan')

################################################################################
# Test fixtures run once for this module
################################################################################

@pytest.fixture(scope='module')
def array_assigned_to_band_1():
    return np.array([[1,2],[3,4]])

@pytest.fixture(scope='module')
def array_assigned_to_band_2():
    return np.array([[11,12],[13,14]])

@pytest.fixture(scope='module')
def dataset(test_dataset_filename, array_assigned_to_band_1, array_assigned_to_band_2):
    '''Create a new dataset, and set its values using write_band() and 
    write_pixel() functions.'''

    # create the new dataset
    dataset = skope.analysis.create_dataset(
        filename     = test_dataset_filename(__file__),
        format       = 'GTiff',
        pixel_type   = gdal.GDT_Float32, 
        rows         = DATASET_ROW_COUNT, 
        cols         = DATASET_COLUMN_COUNT, 
        bands        = DATASET_BAND_COUNT,
        origin_x     = DATASET_ORIGIN_LONGITUDE,
        origin_y     = DATASET_ORIGIN_LATITUDE,
        pixel_width  = DATASET_PIXEL_SIZE_LONGITUDE,
        pixel_height = DATASET_PIXEL_SIZE_LATITUDE,
        coordinate_system='WGS84'
    )

    # set the values in band 1 with a call to write_band
    skope.analysis.write_band(dataset, 1, array_assigned_to_band_1, DATASET_NODATA_VALUE)

    # set the values in band 2 with calls to write_pixel
    skope.analysis.write_pixel(dataset, 2, 0, 0, array_assigned_to_band_2[0,0])
    skope.analysis.write_pixel(dataset, 2, 0, 1, array_assigned_to_band_2[0,1])
    skope.analysis.write_pixel(dataset, 2, 1, 0, array_assigned_to_band_2[1,0])
    skope.analysis.write_pixel(dataset, 2, 1, 1, array_assigned_to_band_2[1,1])

    return dataset

################################################################################
# Tests of dataset read and write functions
# ################################################################################

def test_write_band_sets_assigns_expected_pixel_values(dataset, array_assigned_to_band_1):
    assert np.array_equal(
        array_assigned_to_band_1, 
        dataset.GetRasterBand(1).ReadAsArray()
    )
    
def test_write_pixel_sets_assigns_expected_pixel_values(dataset, array_assigned_to_band_2):
    assert np.array_equal(
        array_assigned_to_band_2, 
        dataset.GetRasterBand(2).ReadAsArray()
    )

def test_read_band_returns_expected_pixel_values(dataset, array_assigned_to_band_1):
    assert np.array_equal(
        array_assigned_to_band_1, 
        skope.analysis.read_band(dataset, 1)
    )

def test_read_pixel_returns_expected_pixel_values(dataset, array_assigned_to_band_2):
    assert array_assigned_to_band_2[0,0] == skope.analysis.read_pixel(dataset, 2, 0, 0)
    assert array_assigned_to_band_2[0,1] == skope.analysis.read_pixel(dataset, 2, 0, 1)
    assert array_assigned_to_band_2[1,0] == skope.analysis.read_pixel(dataset, 2, 1, 0)
    assert array_assigned_to_band_2[1,1] == skope.analysis.read_pixel(dataset, 2, 1, 1)
