'''Tests of the write_pixel, read_pixel, write_band, and read_band functions.'''
import numpy as np
import pytest
from osgeo import gdal

import skope

# pylint: disable=redefined-outer-name

@pytest.fixture(scope='module')
def array_assigned_to_band_index_0():
    '''Return pixel values to be assigned to band index 0.'''
    return np.array([[1, 2], [3, 4]])

@pytest.fixture(scope='module')
def array_assigned_to_band_index_1():
    '''Return pixel values to be assigned to band index 1.'''
    return np.array([[11, 12], [13, 14]])

@pytest.fixture(scope='module')
def raster_dataset(test_dataset_filename,
                   array_assigned_to_band_index_0,
                   array_assigned_to_band_index_1) -> gdal.Dataset:
    '''Create a new dataset, and set its values using write_band() and
    write_pixel() functions.'''

    # create the new dataset
    raster_dataset = skope.RasterDataset.new(test_dataset_filename(__file__),
                                             'GTiff', gdal.GDT_Float32,
                                             shape=(2, 2, 2),
                                             origin=(-123, 45),
                                             pixel_size=(1.0, 1.0),
                                             coordinate_system='WGS84')

    # set the values in band 1 with a call to write_band
    raster_dataset.write_band(0, array_assigned_to_band_index_0, float('Nan'))

    # set the values in band 2 with calls to write_pixel
    raster_dataset.write_pixel(1, 0, 0, array_assigned_to_band_index_1[0, 0])
    raster_dataset.write_pixel(1, 0, 1, array_assigned_to_band_index_1[0, 1])
    raster_dataset.write_pixel(1, 1, 0, array_assigned_to_band_index_1[1, 0])
    raster_dataset.write_pixel(1, 1, 1, array_assigned_to_band_index_1[1, 1])

    return raster_dataset

# pylint: disable=redefined-outer-name, missing-docstring, line-too-long

def test_write_band_sets_assigns_expected_pixel_values(
        raster_dataset: skope.RasterDataset, array_assigned_to_band_index_0):
    assert np.array_equal(
        array_assigned_to_band_index_0,
        raster_dataset.gdal_dataset.GetRasterBand(1).ReadAsArray()
    )

def test_write_pixel_sets_assigns_expected_pixel_values(
        raster_dataset: skope.RasterDataset, array_assigned_to_band_index_1):
    assert np.array_equal(
        array_assigned_to_band_index_1,
        raster_dataset.gdal_dataset.GetRasterBand(2).ReadAsArray()
    )

def test_read_band_returns_expected_pixel_values(
        raster_dataset: skope.RasterDataset, array_assigned_to_band_index_0):
    assert np.array_equal(
        array_assigned_to_band_index_0,
        raster_dataset.read_band(0)
    )

def test_read_pixel_returns_expected_pixel_values(
        raster_dataset: skope.RasterDataset, array_assigned_to_band_index_1):
    assert raster_dataset.read_pixel(1, 0, 0) == array_assigned_to_band_index_1[0, 0]
    assert raster_dataset.read_pixel(1, 0, 1) == array_assigned_to_band_index_1[0, 1]
    assert raster_dataset.read_pixel(1, 1, 0) == array_assigned_to_band_index_1[1, 0]
    assert raster_dataset.read_pixel(1, 1, 1) == array_assigned_to_band_index_1[1, 1]
