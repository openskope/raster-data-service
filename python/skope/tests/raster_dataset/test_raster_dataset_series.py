import numpy
import pytest
import skope

from osgeo import gdal
from skope import RasterDataset

################################################################################
# Module-scoped constants defining properties of the test dataset.
################################################################################

DATASET_ROW_COUNT            = 2
DATASET_COLUMN_COUNT         = 2
DATASET_BAND_COUNT           = 10
DATASET_ORIGIN_LONGITUDE     = -123
DATASET_ORIGIN_LATITUDE      = 45
DATASET_PIXEL_WIDTH          = 1.0
DATASET_PIXEL_HEIGHT         = 1.0
DATASET_NODATA_VALUE         = float('nan')

################################################################################
# Test fixtures run once for this module.
################################################################################

@pytest.fixture(scope='module')
def array_assigned_to_band_index_0():
    return numpy.array([[1,2],[3,4]])

@pytest.fixture(scope='module')
def raster_dataset(test_dataset_filename, 
                   array_assigned_to_band_index_0) -> RasterDataset:

    datafile_path = test_dataset_filename(__file__)

    gdal_dataset = skope.create_dataset(
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
    for band_index in range(0,DATASET_BAND_COUNT):    
        skope.write_band(
            gdal_dataset, 
            band_index, 
            array_assigned_to_band_index_0 + 10 * band_index, 
            DATASET_NODATA_VALUE)

    gdal_dataset = None

    return skope.RasterDataset(datafile_path)


################################################################################
# Tests of raster dataset series functions.
################################################################################

def test_series_returns_numpy_ndarray(raster_dataset: RasterDataset):
    assert isinstance(raster_dataset.series_at_pixel(0,0), numpy.ndarray)

def test_series_returns_band_count_elments(raster_dataset: RasterDataset):
    assert len(raster_dataset.series_at_pixel(0,0)) == DATASET_BAND_COUNT

def test_series_returns_array_with_correct_values(raster_dataset: RasterDataset):
    series_array = raster_dataset.series_at_pixel(0,0) 
    assert series_array[0] == 1
    assert series_array[1] == 11

def test_series_at_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert ( raster_dataset.series_at_pixel(0,0).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0, 51.0, 61.0, 71.0, 81.0, 91.0] )

def test_series_at_pixel_0_1_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(0,1).tolist() == [2.0, 12.0, 22.0, 32.0, 42.0, 52.0, 62.0, 72.0, 82.0, 92.0]

def test_series_at_pixel_1_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(1,0).tolist() == [3.0, 13.0, 23.0, 33.0, 43.0, 53.0, 63.0, 73.0, 83.0, 93.0]

def test_series_at_pixel_1_1_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(1,1).tolist() == [4.0, 14.0, 24.0, 34.0, 44.0, 54.0, 64.0, 74.0, 84.0, 94.0]

def test_series_at_point_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,45).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0, 51.0, 61.0, 71.0, 81.0, 91.0]

def test_series_at_point_in_pixel_0_1_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-122,45).tolist() == [2.0, 12.0, 22.0, 32.0, 42.0, 52.0, 62.0, 72.0, 82.0, 92.0]

def test_series_at_point_in_pixel_1_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,44).tolist() == [3.0, 13.0, 23.0, 33.0, 43.0, 53.0, 63.0, 73.0, 83.0, 93.0]

def test_series_at_point_in_pixel_1_1_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-122,44).tolist() == [4.0, 14.0, 24.0, 34.0, 44.0, 54.0, 64.0, 74.0, 84.0, 94.0]

def test_range_from_0_at_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(0,0,0).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0, 51.0, 61.0, 71.0, 81.0, 91.0]

def test_range_from_0_to_None_at_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(0,0,0,None).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0, 51.0, 61.0, 71.0, 81.0, 91.0]

def test_range_0_to_5_of_series_at_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(0,0,0,5).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0]

def test_range_None_to_5_of_series_at_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(0,0,None,5).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0]

def test_range_to_5_of_series_at_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(0,0,end=5).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0]

def test_range_5_to_10_of_series_at_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(0,0,5,10).tolist() == [51.0, 61.0, 71.0, 81.0, 91.0]

def test_range_5_to_None_of_series_at_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(0,0,5).tolist() == [51.0, 61.0, 71.0, 81.0, 91.0]

def test_range_5_to_5_of_series_at_pixel_0_0_is_empty_array(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(0,0,5,5).tolist() == []

def test_range_5_to_6_of_series_at_pixel_0_0_is_single_element_array(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_pixel(0,0,5,6).tolist() == [51.0]

def test_range_from_0_at_point_in_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,45,0).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0, 51.0, 61.0, 71.0, 81.0, 91.0]

def test_range_from_0_to_None_at_point_in_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,45,0,None).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0, 51.0, 61.0, 71.0, 81.0, 91.0]

def test_range_0_to_5_of_series_at_point_in_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,45,0,5).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0]

def test_range_None_to_5_of_series_at_point_in_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,45,None,5).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0]

def test_range_to_5_of_series_at_point_in_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,45,end=5).tolist() == [1.0, 11.0, 21.0, 31.0, 41.0]

def test_range_5_to_10_of_series_at_point_in_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,45,5,10).tolist() == [51.0, 61.0, 71.0, 81.0, 91.0]

def test_range_5_to_None_of_series_at_point_in_pixel_0_0_is_correct(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,45,5).tolist() == [51.0, 61.0, 71.0, 81.0, 91.0]

def test_range_5_to_5_of_series_at_point_in_pixel_0_0_is_empty_array(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,45,5,5).tolist() == []

def test_range_5_to_6_of_series_at_point_in_pixel_0_0_is_single_element_array(raster_dataset: RasterDataset):
    assert raster_dataset.series_at_point(-123,45,5,6).tolist() == [51.0]
