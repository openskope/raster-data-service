import pytest
import os
from osgeo import gdal
import affine
import skope_analysis

################################################################################
# Test fixtures run once for this module
################################################################################

@pytest.fixture(scope='module')
def dataset_directory(tmpdir_factory):
    ''' create a temporary directory for storing the new dataset file '''
    return tmpdir_factory.mktemp('dataset_directory')

@pytest.fixture(scope='module')
def path_to_dataset(dataset_directory):
    ''' create a new dataset file and return its path'''
    path_to_dataset = str(dataset_directory) + 'test.tif'
    skope_analysis.create_dataset_file(
        filename     = path_to_dataset,
        format       = 'GTiff',
        pixel_type   = gdal.GDT_Float32, 
        rows         = 4, 
        cols         = 5, 
        bands        = 6,
        origin_x     = -123,
        origin_y     = 45,
        pixel_width  = 1,
        pixel_height = 2,
        coordinate_system='WGS84'
    )
    return path_to_dataset

@pytest.fixture(scope='module')
def dataset(path_to_dataset):
    ''' open the new dataset file with GDAL and return a gdal.Dataset object '''
    return gdal.Open(path_to_dataset)

@pytest.fixture(scope='module')
def metadata(dataset):
    ''' return the metadata dictionary for the new dataset '''
    return dataset.GetMetadata_Dict()

@pytest.fixture(scope='module')
def geotransform(dataset):
    ''' return the geotransform array for the new dataset '''
    return dataset.GetGeoTransform()

@pytest.fixture(scope='module')
def affine_matrix(geotransform):
    ''' return the affine matrix for the projection '''
    return affine.Affine.from_gdal(geotransform[0], geotransform[1],
                                   geotransform[2], geotransform[3],
                                   geotransform[4], geotransform[5])

@pytest.fixture(scope='module')
def inverse_affine(affine_matrix):
    ''' return the inverse affine matrix for the projection '''
    return ~affine_matrix

@pytest.fixture(scope='module')
def first_band(dataset):
    ''' return band 1 of the new dataset '''
    return dataset.GetRasterBand(1) 

################################################################################
# Tests of the results of using the create_dataset_file() function
################################################################################

def test_created_datafile_exists(path_to_dataset):
    assert os.path.isfile(path_to_dataset) 

def test_dataset_object_is_gdal_dataset(dataset):
    assert str((type(dataset))) == "<class 'osgeo.gdal.Dataset'>"

def test_dataset_format_is_geotiff(dataset):
     assert dataset.GetDriver().LongName == 'GeoTIFF'

def test_pixel_type_is_float32(first_band):
     assert gdal.GetDataTypeName(first_band.DataType) == 'Float32'

def test_dataset_height_in_pixels_is_4(dataset):
    assert dataset.RasterYSize == 4

def test_dataset_width_in_pixels_is_5(dataset):
    assert dataset.RasterXSize == 5

def test_dataset_band_count_is_6(dataset):
    assert dataset.RasterCount == 6

def test_pixel_width_is_1(geotransform):
    assert geotransform[1] == 1.0

def test_pixel_height_is_2(geotransform):
    assert geotransform[5] == 2.0

def test_geotransform_is_north_up(geotransform):
    assert (geotransform[2],geotransform[4]) == (0,0)

def test_projection_is_wgs84(dataset):
    assert dataset.GetProjection()[8:14] == 'WGS 84'

def test_geotransform_origin_is_at_123_w_45_n(geotransform):
    assert (geotransform[0], geotransform[3]) == (-123, 45)

def test_projected_coordinates_of_pixel_0_0_is_origin(affine_matrix):
    assert (affine_matrix * (0, 0)) == (-123.0, 45.0)

def test_inverse_projection_of_origin_is_pixel_0_0(inverse_affine):
    assert (inverse_affine * (-123.0, 45.0)) == (0, 0)
