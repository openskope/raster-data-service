'''Tests of the RasterDataset factory method.'''

import os
from typing import List, Dict

import pytest
from osgeo import gdal
from skope import RasterDataset

# pylint: disable=redefined-outer-name

@pytest.fixture(scope='module')
def raster_dataset(test_dataset_filename) -> RasterDataset:
    '''Return a new RasterDataset built by the factory function.'''
    return RasterDataset.create(test_dataset_filename(__file__), 'GTiff',
                                gdal.GDT_Float32, shape=(6, 4, 5),
                                origin=(-123.0, 45.0), pixel_size=(1.0, 2.0),
                                coordinate_system='WGS84')

@pytest.fixture(scope='module')
def gdal_dataset(raster_dataset) -> gdal.Dataset:
    '''Return the gdal datset backing the new RasterDataset.'''
    return raster_dataset._gdal_dataset # pylint: disable=protected-access

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

# pylint: disable=redefined-outer-name, missing-docstring, line-too-long

def test_fixture_is_instance_of_raster_dataset(raster_dataset: RasterDataset):
    assert str((type(raster_dataset))) == "<class 'skope.raster_dataset.RasterDataset'>"

def test_created_datafile_exists(raster_dataset: RasterDataset):
    assert os.path.isfile(raster_dataset.filename)

def test_dataset_format_is_geotiff(gdal_dataset: gdal.Dataset):
    assert gdal_dataset.GetDriver().LongName == "GeoTIFF"

def test_pixel_type_is_float32(first_band: gdal.Band):
    assert gdal.GetDataTypeName(first_band.DataType) == 'Float32'

def test_dataset_height_in_pixels_is_4(gdal_dataset: gdal.Dataset):
    assert gdal_dataset.RasterYSize == 4

def test_dataset_width_in_pixels_is_5(gdal_dataset: gdal.Dataset):
    assert gdal_dataset.RasterXSize == 5

def test_dataset_band_count_is_6(gdal_dataset: gdal.Dataset):
    assert gdal_dataset.RasterCount == 6

def test_pixel_width_is_1(geotransform: List[float]):
    assert geotransform[1] == 1.0

def test_pixel_height_is_2(geotransform: List[float]):
    assert geotransform[5] == -2.0

def test_geotransform_is_north_up(geotransform: List[float]):
    assert (geotransform[2], geotransform[4]) == (0, 0)

def test_projection_is_wgs84(gdal_dataset: gdal.Dataset):
    assert gdal_dataset.GetProjection()[8:14] == 'WGS 84'

def test_geotransform_origin_is_at_123_w_45_n(geotransform: List[float]):
    assert (geotransform[0], geotransform[3]) == (-123.0, 45.0)
