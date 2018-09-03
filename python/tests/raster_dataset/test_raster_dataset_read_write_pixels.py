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
# Tests of raster dataset pixel read function.
################################################################################

def test_value_at_pixel_returns_value_of_each_pixel_in_dataset(raster_dataset):
    assert raster_dataset.value_at_pixel(row=0, column=0, band=1) == 1
    assert raster_dataset.value_at_pixel(row=0, column=1, band=1) == 2
    assert raster_dataset.value_at_pixel(row=1, column=0, band=1) == 3
    assert raster_dataset.value_at_pixel(row=1, column=1, band=1) == 4
    assert raster_dataset.value_at_pixel(row=0, column=0, band=2) == 11
    assert raster_dataset.value_at_pixel(row=0, column=1, band=2) == 12
    assert raster_dataset.value_at_pixel(row=1, column=0, band=2) == 13
    assert raster_dataset.value_at_pixel(row=1, column=1, band=2) == 14

def test_value_at_point_returns_value_at_0_0_for_origin(raster_dataset):
    assert raster_dataset.value_at_point(-123, 45, band=1) == 1
    assert raster_dataset.value_at_point(-123, 45, band=2) == 11

def test_value_at_point_returns_value_at_1_1_near_southeast_corner(raster_dataset):
    assert raster_dataset.value_at_point(-121.001, 43.001, band=1) == 4
    assert raster_dataset.value_at_point(-121.001, 43.001, band=2) == 14
