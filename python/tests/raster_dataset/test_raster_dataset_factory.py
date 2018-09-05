import affine
import numpy as np
import os
import pytest
import skope.analysis

from osgeo import gdal
from skope.analysis import RasterDataset
from typing import List, Dict

################################################################################
# Module-scoped constants defining properties of the test dataset.
################################################################################

DATASET_ROW_COUNT            = 4
DATASET_COLUMN_COUNT         = 5
DATASET_BAND_COUNT           = 6
DATASET_ORIGIN_LONGITUDE     = -123
DATASET_ORIGIN_LATITUDE      = 45
DATASET_PIXEL_WIDTH          = 1.0
DATASET_PIXEL_HEIGHT         = 2.0

################################################################################
# Test fixtures run once for this module.
################################################################################

@pytest.fixture(scope='module')
def raster_dataset(test_dataset_filename) -> RasterDataset:
    '''Return a new RasterDataset built by the factory function.'''
    return RasterDataset.new(
        filename     = test_dataset_filename(__file__),
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

@pytest.fixture(scope='module')
def gdal_dataset(raster_dataset) -> gdal.Dataset:
    '''Return the gdal datset backing the new RasterDataset.'''
    return raster_dataset.gdal_dataset

@pytest.fixture(scope='module')
def metadata(gdal_dataset) -> Dict:
    '''Return the metadata dictionary for the new dataset.'''
    return gdal_dataset.GetMetadata_Dict()

@pytest.fixture(scope='module')
def geotransform(gdal_dataset) -> List[float]:
    '''Return the geotransform array for the new dataset.'''
    return gdal_dataset.GetGeoTransform()

@pytest.fixture(scope='module')
def first_band(gdal_dataset) -> gdal.Band:
    '''Return band 1 of the new dataset.'''
    return gdal_dataset.GetRasterBand(1)

################################################################################
# Tests of the results of using the RasterDataset factory function.
################################################################################

def test_fixture_is_instance_of_raster_dataset(raster_dataset: RasterDataset):
    assert str((type(raster_dataset))) == "<class 'skope.analysis.raster_dataset.RasterDataset'>"

def test_created_datafile_exists(raster_dataset: RasterDataset):
    assert os.path.isfile(raster_dataset.filename) 

def test_dataset_format_is_geotiff(gdal_dataset: gdal.Dataset):
     assert gdal_dataset.GetDriver().LongName == "GeoTIFF"

def test_pixel_type_is_float32(first_band: gdal.Band):
     assert gdal.GetDataTypeName(first_band.DataType) == 'Float32'

def test_dataset_height_in_pixels_is_4(gdal_dataset: gdal.Dataset):
    assert gdal_dataset.RasterYSize == DATASET_ROW_COUNT

def test_dataset_width_in_pixels_is_5(gdal_dataset: gdal.Dataset):
    assert gdal_dataset.RasterXSize == DATASET_COLUMN_COUNT

def test_dataset_band_count_is_6(gdal_dataset: gdal.Dataset):
    assert gdal_dataset.RasterCount == DATASET_BAND_COUNT

def test_pixel_width_is_1(geotransform: List[float]):
    assert geotransform[1] == DATASET_PIXEL_WIDTH

def test_pixel_height_is_2(geotransform: List[float]):
    assert geotransform[5] == -DATASET_PIXEL_HEIGHT

def test_geotransform_is_north_up(geotransform: List[float]):
    assert (geotransform[2],geotransform[4]) == (0,0)

def test_projection_is_wgs84(gdal_dataset: gdal.Dataset):
    assert gdal_dataset.GetProjection()[8:14] == 'WGS 84'

def test_geotransform_origin_is_at_123_w_45_n(geotransform: List[float]):
    assert (geotransform[0], geotransform[3]) == (-123.0, 45.0)
