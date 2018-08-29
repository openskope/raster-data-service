import pytest
import skope.analysis
import numpy as np
from osgeo import gdal

################################################################################
# Constants defined for this module.
################################################################################

FILE_FORMAT     = 'GTiff'
DATA_TYPE       = gdal.GDT_Float32
ROW_COUNT       = 4
COLUMN_COUNT    = 5
BAND_COUNT      = 6
ORIGIN_X        = -123
ORIGIN_Y        = 45
PIXEL_SIZE_X    = 1.0
PIXEL_SIZE_Y    = 2.0
COORDINATE_SYS  = 'WGSG4'

################################################################################
# Test fixtures run once for this module
################################################################################

@pytest.fixture(scope='module')
def dataset_directory(tmpdir_factory):
    '''Create a temporary directory for storing the new dataset file.'''
    return tmpdir_factory.mktemp('dataset_directory')

@pytest.fixture(scope='module')
def dataset(dataset_directory):
    '''Create a new dataset file and return its path.'''
    dataset = skope.analysis.create_dataset(
        filename          = str(dataset_directory) + 'test.tif',
        format            = FILE_FORMAT,
        pixel_type        = DATA_TYPE, 
        rows              = ROW_COUNT, 
        cols              = COLUMN_COUNT, 
        bands             = BAND_COUNT,
        origin_x          = ORIGIN_X,
        origin_y          = ORIGIN_X,
        pixel_width       = PIXEL_SIZE_X,
        pixel_height      = PIXEL_SIZE_Y,
        coordinate_system = COORDINATE_SYS
    )
    return dataset

################################################################################
# Tests of coordinate transformation functions
# ################################################################################

# def test_pixel_for_geospatial_origin_is_0_0(dataset):
#     assert (0,0) == skope.analysis.get_pixel_indices_for_point(dataset, ORIGIN_X, ORIGIN_Y)

#def test_pixel_coordinates_of_geospatial_origin_is_0_0(dataset):
#    assert (0,0) == skope.analysis.get_pixel_indices_for_point(dataset, ORIGIN_X + PIXEL_SIZE_X/2, ORIGIN_Y - PIXEL_SIZE_Y/2)
