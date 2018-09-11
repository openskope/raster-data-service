'''Tests of the RasterDataset constructor.'''
import pytest

from affine import Affine
from osgeo import gdal

import skope
from skope import RasterDataset

# pylint: disable=redefined-outer-name

@pytest.fixture(scope='module')
def valid_dataset_filename(test_dataset_filename) -> str:
    '''Return a new gdal.Dataset instance'''
    valid_dataset_filename = test_dataset_filename(__file__)
    skope.create_dataset(valid_dataset_filename, 'GTiff', gdal.GDT_Float32,
                         rows=3, cols=2, bands=4, origin_long=-123,
                         origin_lat=45, pixel_width=1.0, pixel_height=2.0,
                         coordinate_system='WGS84')
    return valid_dataset_filename

@pytest.fixture(scope='module')
def valid_gdal_dataset(valid_dataset_filename: str) -> gdal.Dataset:
    '''Open the new dataset file with GDAL and return a gdal.Dataset object.'''
    return skope.open_dataset(valid_dataset_filename)

@pytest.fixture(scope='module')
def invalid_dataset_filename(test_dataset_filename: str):
    '''Return the path to an empty text file representing an invalid dataset file.'''
    invalid_dataset_filename = test_dataset_filename(__file__, ".txt")
    open(invalid_dataset_filename, 'w').close()
    return invalid_dataset_filename

@pytest.fixture(scope='module')
def expected_type_error_message() -> str:
    '''Return the error message expected when an unexpected type is passed
    to the RasterDataset constructor.'''
    return 'Expected a gdal.Dataset object or a string representing the path to a datafile.'

@pytest.fixture(scope='module')
def expected_file_not_found_error_message() -> str:
    '''Return the error message expected when the argument to the RasterDataset
    constructor is a string but no file is found at the path given by that string.'''
    return 'Dataset file not found at path'

@pytest.fixture(scope='module')
def expected_invalid_dataset_file_error_message() -> str:
    '''Return the error message expected when the file referred to a string
    argument to the RasterDataset constructor is not a GDAL-compatible data file.'''
    return 'Invalid dataset file found at path'

# pylint: disable=redefined-outer-name, missing-docstring, line-too-long

def test_when_constructor_argument_is_none_a_datatype_exception_is_raised(
        expected_type_error_message: str
    ):
    with pytest.raises(TypeError, match=expected_type_error_message):
        skope.RasterDataset(None)

def test_when_constructor_argument_is_int_an_exception_is_raised(
        expected_type_error_message: str
    ):
    with pytest.raises(TypeError, match=expected_type_error_message):
        skope.RasterDataset(1)

def test_when_constructor_argument_is_invalid_string_an_exception_is_raised(
        expected_file_not_found_error_message: str
    ):
    with pytest.raises(FileNotFoundError, match=expected_file_not_found_error_message):
        skope.RasterDataset("path_to_nonexistent_file")

def test_when_constructor_argument_is_a_gdal_dataset_properties_are_correct(
        valid_gdal_dataset: gdal.Dataset
    ):
    raster_dataset = RasterDataset(valid_gdal_dataset)
    assert raster_dataset.filename is None
    assert raster_dataset.gdal_dataset == valid_gdal_dataset
    assert raster_dataset.shape == (4, 3, 2)
    assert raster_dataset.bands == 4
    assert raster_dataset.rows == 3
    assert raster_dataset.cols == 2
    assert raster_dataset.affine == Affine(1.0, 0.0, -123.0, 0.0, -2.0, 45.0)
    assert raster_dataset.pixel_size == (1.0, 2.0)
    assert raster_dataset.pixel_size_x == 1.0
    assert raster_dataset.pixel_size_y == 2.0
    assert raster_dataset.origin == (-123, 45)
    assert raster_dataset.origin_long == -123
    assert raster_dataset.origin_lat == 45
    assert raster_dataset.northwest_corner == (-123, 45)
    assert raster_dataset.southwest_corner == (-123, 39)
    assert raster_dataset.northeast_corner == (-121, 45)
    assert raster_dataset.southeast_corner == (-121, 39)
    assert raster_dataset.center == (-122, 42)

def test_when_constructor_argument_is_path_to_dataset_properties_are_correct(
        valid_dataset_filename: str
    ):
    raster_dataset = RasterDataset(valid_dataset_filename)
    assert raster_dataset.filename == valid_dataset_filename
    assert raster_dataset.shape == (4, 3, 2)
    assert raster_dataset.bands == 4
    assert raster_dataset.rows == 3
    assert raster_dataset.cols == 2
    assert raster_dataset.affine == Affine(1.0, 0.0, -123.0, 0.0, -2.0, 45.0)
    assert raster_dataset.pixel_size == (1.0, 2.0)
    assert raster_dataset.pixel_size_x == 1.0
    assert raster_dataset.pixel_size_y == 2.0
    assert raster_dataset.origin == (-123, 45)
    assert raster_dataset.origin_long == -123
    assert raster_dataset.origin_lat == 45
    assert raster_dataset.northwest_corner == (-123, 45)
    assert raster_dataset.southwest_corner == (-123, 39)
    assert raster_dataset.northeast_corner == (-121, 45)
    assert raster_dataset.southeast_corner == (-121, 39)
    assert raster_dataset.center == (-122, 42)

def test_when_constructor_argument_is_path_to_invalid_dataset_file_an_exception_is_raised(
        invalid_dataset_filename: str,
        expected_invalid_dataset_file_error_message: str
    ):
    with pytest.raises(ValueError, match=expected_invalid_dataset_file_error_message):
        RasterDataset(invalid_dataset_filename)
