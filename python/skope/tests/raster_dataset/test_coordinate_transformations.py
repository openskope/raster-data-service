'''Tests of the RasterDataset coordinate properties and methods.'''

import pytest

from osgeo import gdal
from skope import RasterDataset

# pylint: disable=redefined-outer-name

@pytest.fixture(scope='module')
def raster_dataset(test_dataset_filename) -> RasterDataset:
    '''Return a new RasterDataset.'''
    return RasterDataset.create(test_dataset_filename(__file__), 'GTiff',
                                gdal.GDT_Float32, shape=(6, 4, 5),
                                origin=(-123, 45), pixel_size=(1.0, 2.0),
                                coordinate_system='WGS84')

# pylint: disable=redefined-outer-name, missing-docstring, line-too-long

def test_pixel_size(raster_dataset: RasterDataset):
    assert raster_dataset.pixel_size == (1, 2)

def test_origin(raster_dataset: RasterDataset):
    assert raster_dataset.origin == (-123, 45)

def test_northwest_corner(raster_dataset: RasterDataset):
    assert raster_dataset.northwest_corner == (-123, 45)

def test_northeast_corner(raster_dataset: RasterDataset):
    assert raster_dataset.northeast_corner == (-118, 45)

def test_southeast_corner(raster_dataset: RasterDataset):
    assert raster_dataset.southeast_corner == (-118, 37)

def test_southwest_corner(raster_dataset: RasterDataset):
    assert raster_dataset.southwest_corner == (-123, 37)

def test_center(raster_dataset: RasterDataset):
    assert raster_dataset.center == (-120.5, 41)

def test_pixel_at_origin_is_0_0(raster_dataset: RasterDataset):
    assert raster_dataset.pixel_at_point(-123, 45) == (0, 0)

def test_pixel_at_point_at_center_of_northwest_pixel_is_0_0(raster_dataset: RasterDataset):
    assert raster_dataset.pixel_at_point(-122.5, 44) == (0, 0)

def test_pixel_at_point_just_northwest_of_southeast_corner_of_northwest_pixel_is_0_0(raster_dataset: RasterDataset):
    assert raster_dataset.pixel_at_point(-122.001, 43.001) == (0, 0)

def test_pixel_at_point_just_southeast_of_southwest_corner_of_northwest_pixel_is_0_0(raster_dataset: RasterDataset):
    assert raster_dataset.pixel_at_point(-121.999, 42.999) == (1, 1)

def test_pixel_at_point_just_northwest_of_northwest_corner_of_northwest_pixel_is_outside_coverage(raster_dataset: RasterDataset):
    assert raster_dataset.pixel_at_point(-123.001, 45.001) is None

def test_pixel_at_point_just_northwest_of_southeast_corner_of_southeast_pixel_is_boottom_right_pixel(raster_dataset: RasterDataset):
    assert raster_dataset.pixel_at_point(-118.001, 37.001) == (3, 4)

def test_pixel_at_point_just_southeast_of_southeast_corner_of_southeast_pixel_is_outside_coverage(raster_dataset: RasterDataset):
    assert raster_dataset.pixel_at_point(-117.999, 36.999) is None
