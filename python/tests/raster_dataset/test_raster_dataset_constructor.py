import pytest
import skope.analysis

from affine import Affine
from osgeo import gdal

################################################################################
# Module-scoped constants defining properties of the test dataset.
################################################################################

DATASET_BAND_COUNT           = 4
DATASET_ROW_COUNT            = 3
DATASET_COLUMN_COUNT         = 2
DATASET_ORIGIN_LONGITUDE     = -123
DATASET_ORIGIN_LATITUDE      = 45
DATASET_PIXEL_WIDTH          = 1.0
DATASET_PIXEL_HEIGHT         = 2.0
DATASET_NODATA_VALUE         = float('nan')

################################################################################
# Test fixtures run once for this module.
################################################################################

@pytest.fixture(scope='module')
def valid_dataset_filename(test_dataset_filename):
    '''Return a new gdal.Dataset instance'''
    valid_dataset_filename = test_dataset_filename(__file__)
    skope.analysis.create_dataset(
        filename     = valid_dataset_filename,
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
    return valid_dataset_filename

@pytest.fixture(scope='module')
def valid_gdal_dataset(valid_dataset_filename):
    '''Open the new dataset file with GDAL and return a gdal.Dataset object.'''
    return skope.analysis.open_dataset(valid_dataset_filename)

@pytest.fixture(scope='module')
def invalid_dataset_filename(test_dataset_filename):
    '''Return the path to an empty text file representing an invalid dataset file.'''
    invalid_dataset_filename = test_dataset_filename(__file__, ".txt")
    open(invalid_dataset_filename, 'w').close()
    return invalid_dataset_filename

@pytest.fixture(scope='module')
def expected_type_error_message():
    return 'Expected a gdal.Dataset object or a string representing the path to a datafile.'

@pytest.fixture(scope='module')
def expected_file_not_found_error_message():
    return 'Dataset file not found at path'

@pytest.fixture(scope='module')
def expected_invalid_dataset_file_error_message():
    return 'Invalid dataset file found at path'

################################################################################
# Tests of the RasterDataset constructor.
################################################################################

def test_when_constructor_argument_is_none_a_datatype_exception_is_raised(expected_type_error_message):
    with pytest.raises(TypeError, match=expected_type_error_message):
        skope.analysis.RasterDataset(None)

def test_when_constructor_argument_is_int_an_exception_is_raised(expected_type_error_message):
    with pytest.raises(TypeError, match=expected_type_error_message):
        skope.analysis.RasterDataset(1)

def test_when_constructor_argument_is_invalid_string_an_exception_is_raised(expected_file_not_found_error_message):
    with pytest.raises(FileNotFoundError, match=expected_file_not_found_error_message):
        skope.analysis.RasterDataset("path_to_nonexistent_file")

def test_when_constructor_argument_is_a_gdal_dataset_properties_are_correct(valid_gdal_dataset):
    raster_dataset = skope.analysis.RasterDataset(valid_gdal_dataset)
    assert raster_dataset.filename == None
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

def test_when_constructor_argument_is_path_to_dataset_properties_are_correct(valid_dataset_filename):
    raster_dataset = skope.analysis.RasterDataset(valid_dataset_filename)
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

def test_when_constructor_argument_is_path_to_invalid_dataset_file_an_exception_is_raised(invalid_dataset_filename, expected_invalid_dataset_file_error_message):
    with pytest.raises(ValueError, match=expected_invalid_dataset_file_error_message):
        skope.analysis.RasterDataset(invalid_dataset_filename)