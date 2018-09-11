'''Tests of the skope.create_dataset function.'''
import os
from typing import List, Dict

import affine
import numpy as np
import pytest
from osgeo import gdal

import skope

# pylint: disable=redefined-outer-name

@pytest.fixture(scope='module')
def path_to_dataset(test_dataset_filename) -> str:
    '''Create a new dataset file and return its path.'''
    path_to_dataset = test_dataset_filename(__file__)
    skope.create_dataset(filename=path_to_dataset, file_format='GTiff',
                         pixel_type=gdal.GDT_Float32, rows=4, cols=5,
                         bands=6, origin_long=-123, origin_lat=45,
                         pixel_width=1.0, pixel_height=2.0,
                         coordinate_system='WGS84')
    return path_to_dataset

@pytest.fixture(scope='module')
def dataset(path_to_dataset) -> gdal.Dataset:
    '''Open the new dataset file with GDAL and return a gdal.Dataset object.'''
    return skope.open_dataset(path_to_dataset)

@pytest.fixture(scope='module')
def metadata(dataset) -> Dict:
    '''Return the metadata dictionary for the new dataset.'''
    return dataset.GetMetadata_Dict()

@pytest.fixture(scope='module')
def geotransform(dataset) -> List[float]:
    '''Return the geotransform array for the new dataset.'''
    return dataset.GetGeoTransform()

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
def first_band(dataset) -> gdal.Band:
    '''Return band 1 of the new dataset.'''
    return dataset.GetRasterBand(1)

# pylint: disable=redefined-outer-name, missing-docstring, line-too-long

def test_created_datafile_exists(path_to_dataset: str):
    assert os.path.isfile(path_to_dataset)

def test_dataset_object_is_gdal_dataset(dataset: gdal.Dataset):
    assert str((type(dataset))) == "<class 'osgeo.gdal.Dataset'>"

def test_dataset_format_is_geotiff(dataset: gdal.Dataset):
    assert dataset.GetDriver().LongName == "GeoTIFF"

def test_pixel_type_is_float32(first_band: gdal.Band):
    assert gdal.GetDataTypeName(first_band.DataType) == 'Float32'

def test_dataset_height_in_pixels_is_4(dataset: gdal.Dataset):
    assert dataset.RasterYSize == 4

def test_dataset_width_in_pixels_is_5(dataset: gdal.Dataset):
    assert dataset.RasterXSize == 5

def test_dataset_band_count_is_6(dataset: gdal.Dataset):
    assert dataset.RasterCount == 6

def test_pixel_width_is_1(geotransform: List[float]):
    assert geotransform[1] == 1.0

def test_pixel_height_is_2(geotransform: List[float]):
    assert geotransform[5] == -2.0

def test_geotransform_is_north_up(geotransform: List[float]):
    assert (geotransform[2], geotransform[4]) == (0, 0)

def test_projection_is_wgs84(dataset: gdal.Dataset):
    assert dataset.GetProjection()[8:14] == 'WGS 84'

def test_geotransform_origin_is_at_123_w_45_n(geotransform: List[float]):
    assert (geotransform[0], geotransform[3]) == (-123.0, 45.0)

def test_projected_coordinates_of_pixel_0_0_is_northwest_corner(affine_matrix: List[float]):
    assert (affine_matrix * (0, 0)) == (-123.0, 45.0)

def test_inverse_projection_of_northwest_corner_is_pixel_0_0(inverse_affine: List[float]):
    assert (inverse_affine * (-123.0, 45.0)) == (0, 0)

def test_projected_coordinates_of_pixel_4_3_is_southeast_corner(affine_matrix: List[float]):
    assert (affine_matrix * (5, 4)) == (-118.0, 37.0)

def test_inverse_projection_of_southeast_corner_is_pixel_5_4(inverse_affine: List[float]):
    assert (inverse_affine * (-118.0, 37.0)) == (5, 4)

@pytest.mark.parametrize("band_index", range(0, 6))
def test_initial_pixel_values_all_zero_in_band(dataset: gdal.Dataset, band_index: int):
    band_number = band_index + 1
    band_pixels = dataset.GetRasterBand(band_number).ReadAsArray()
    assert np.array_equal(band_pixels, np.array([[0., 0., 0., 0., 0.],
                                                 [0., 0., 0., 0., 0.],
                                                 [0., 0., 0., 0., 0.],
                                                 [0., 0., 0., 0., 0.]]))
