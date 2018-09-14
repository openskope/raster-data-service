'''Test the RasterDataset.create() function by opening the new file using GDAL directly.'''
import os
from typing import List

import affine
import numpy as np
import pytest
from osgeo import gdal

from skope import RasterDataset

# pylint: disable=redefined-outer-name

@pytest.fixture(scope='module')
def path_to_dataset(test_dataset_filename) -> str:
    '''Create a new dataset file and return its path.'''
    path_to_dataset = test_dataset_filename(__file__)
    RasterDataset.create(path_to_dataset, 'GTiff', gdal.GDT_Float32,
                         shape=(6, 4, 5), origin=(-123, 45),
                         pixel_size=(1.0, 2.0),
                         coordinate_system='WGS84')
    return path_to_dataset

@pytest.fixture(scope='module')
def gdal_dataset(path_to_dataset) -> gdal.Dataset:
    '''Open the new dataset file with GDAL and return a gdal.Dataset object.'''
    return gdal.Open(path_to_dataset)

@pytest.fixture(scope='module')
def geotransform(gdal_dataset) -> List[float]:
    '''Return the geotransform array for the new dataset.'''
    return gdal_dataset.GetGeoTransform()

@pytest.fixture(scope='module')
def affine_matrix(geotransform) -> List[float]:
    '''Return the affine matrix for the projection.'''
    return affine.Affine.from_gdal(geotransform[0], geotransform[1],
                                   geotransform[2], geotransform[3],
                                   geotransform[4], geotransform[5])

@pytest.fixture(scope='module')
def inverse_affine(affine_matrix) -> List[float]:
    '''Return the inverse affine matrix for the projection.'''
    return ~affine_matrix

@pytest.fixture(scope='module')
def first_band(gdal_dataset) -> gdal.Band:
    '''Return band 1 of the new dataset.'''
    return gdal_dataset.GetRasterBand(1)

# pylint: disable=redefined-outer-name, missing-docstring, line-too-long

def test_created_datafile_exists(path_to_dataset: str):
    assert os.path.isfile(path_to_dataset)

def test_dataset_object_is_gdal_dataset(gdal_dataset: gdal.Dataset):
    assert str((type(gdal_dataset))) == "<class 'osgeo.gdal.Dataset'>"

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

def test_affine_matrix_is_correct(affine_matrix: List[float]):
    assert affine_matrix == affine.Affine(1.0, 0.0, -123.0, 0.0, -2.0, 45.0)

def test_projected_coordinates_of_pixel_0_0_is_northwest_corner(affine_matrix: List[float]):
    assert (affine_matrix * (0, 0)) == (-123.0, 45.0)

def test_inverse_projection_of_northwest_corner_is_pixel_0_0(inverse_affine: List[float]):
    assert (inverse_affine * (-123.0, 45.0)) == (0, 0)

def test_projected_coordinates_of_pixel_4_3_is_southeast_corner(affine_matrix: List[float]):
    assert (affine_matrix * (5, 4)) == (-118.0, 37.0)

def test_inverse_projection_of_southeast_corner_is_pixel_5_4(inverse_affine: List[float]):
    assert (inverse_affine * (-118.0, 37.0)) == (5, 4)

@pytest.mark.parametrize("band_index", range(0, 6))
def test_initial_pixel_values_all_zero_in_band(gdal_dataset: gdal.Dataset, band_index: int):
    band_number = band_index + 1
    band_pixels = gdal_dataset.GetRasterBand(band_number).ReadAsArray()
    assert np.array_equal(band_pixels, np.array([[0., 0., 0., 0., 0.],
                                                 [0., 0., 0., 0., 0.],
                                                 [0., 0., 0., 0., 0.],
                                                 [0., 0., 0., 0., 0.]]))
