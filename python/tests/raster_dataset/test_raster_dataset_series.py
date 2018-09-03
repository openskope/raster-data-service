import numpy as np
import pytest
import skope.analysis

from osgeo import gdal

################################################################################
# Module-scoped constants defining properties of the test dataset.
################################################################################

DATASET_ROW_COUNT            = 2
DATASET_COLUMN_COUNT         = 2
DATASET_BAND_COUNT           = 2
DATASET_ORIGIN_LONGITUDE     = -123
DATASET_ORIGIN_LATITUDE      = 45
DATASET_PIXEL_WIDTH          = 1.0
DATASET_PIXEL_HEIGHT         = 1.0
DATASET_NODATA_VALUE         = float('nan')

################################################################################
# Test fixtures run once for this module.
################################################################################

@pytest.fixture(scope='module')
def array_assigned_to_band_1():
    return np.array([[1,2],[3,4]])

@pytest.fixture(scope='module')
def array_assigned_to_band_2():
    return np.array([[11,12],[13,14]])

@pytest.fixture(scope='module')
def raster_dataset(test_dataset_filename, array_assigned_to_band_1, array_assigned_to_band_2):

    datafile_path = test_dataset_filename(__file__)

    gdal_dataset = skope.analysis.create_dataset(
        filename     = datafile_path,
        format       = 'GTiff',
        pixel_type   = gdal.GDT_Float32, 
        rows         = DATASET_ROW_COUNT, 
        cols         = DATASET_COLUMN_COUNT, 
        bands        = DATASET_BAND_COUNT,
        origin_long  = DATASET_ORIGIN_LONGITUDE,
        origin_lat   = DATASET_ORIGIN_LATITUDE,
        pixel_width  = DATASET_PIXEL_WIDTH,
        pixel_height = DATASET_PIXEL_HEIGHT,
        coordinate_system='WGS84'
    )

    # set the values in band 1 with a call to write_band
    skope.analysis.write_band(gdal_dataset, 1, array_assigned_to_band_1, DATASET_NODATA_VALUE)
    skope.analysis.write_band(gdal_dataset, 2, array_assigned_to_band_2, DATASET_NODATA_VALUE)

    gdal_dataset = None

    return skope.analysis.RasterDataset(datafile_path)


################################################################################
# Tests of raster dataset series functions.
################################################################################

def test_series_returns_numpy_ndarray(raster_dataset):
    assert isinstance(raster_dataset.series_at_pixel(0,0), np.ndarray)

def test_series_returns_band_count_elments(raster_dataset):
    assert len(raster_dataset.series_at_pixel(0,0)) == DATASET_BAND_COUNT

def test_series_returns_array_with_correct_values(raster_dataset):
    series_array = raster_dataset.series_at_pixel(0,0) 
    assert series_array[0] == 1
    assert series_array[1] == 11

def test_series_at_pixel_0_0_is_correct(raster_dataset):
    assert raster_dataset.series_at_pixel(0,0).tolist() == [1,11]

def test_series_at_pixel_0_1_is_correct(raster_dataset):
    assert raster_dataset.series_at_pixel(0,1).tolist() == [2,12]

def test_series_at_pixel_1_0_is_correct(raster_dataset):
    assert raster_dataset.series_at_pixel(1,0).tolist() == [3,13]

def test_series_at_pixel_1_1_is_correct(raster_dataset):
    assert raster_dataset.series_at_pixel(1,1).tolist() == [4,14]

def test_series_at_point_pixel_0_0_is_correct(raster_dataset):
    assert raster_dataset.series_at_point(-123,45).tolist() == [1,11]

def test_series_at_point_in_pixel_0_1_is_correct(raster_dataset):
    assert raster_dataset.series_at_point(-123,44).tolist() == [2,12]

def test_series_at_point_in_pixel_1_0_is_correct(raster_dataset):
    assert raster_dataset.series_at_point(-122,45).tolist() == [3,13]

def test_series_at_point_in_pixel_1_1_is_correct(raster_dataset):
    assert raster_dataset.series_at_point(-122,44).tolist() == [4,14]