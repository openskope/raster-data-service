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
def dataset(test_dataset_filename,
            array_assigned_to_band_index_0,
            array_assigned_to_band_index_1) -> gdal.Dataset:
    '''Create a new dataset, and set its values using write_band() and
    write_pixel() functions.'''

    # create the new dataset
    dataset = skope.create_dataset(test_dataset_filename(__file__), 'GTiff', gdal.GDT_Float32,
                                   bands=2, rows=2, columns=2,
                                   origin_long=-123, origin_lat=45,
                                   pixel_width=1.0, pixel_height=1.0,
                                   coordinate_system='WGS84')

    # set the values in band 1 with a call to write_band
    skope.write_band(dataset, 0, array_assigned_to_band_index_0, float('Nan'))

    # set the values in band 2 with calls to write_pixel
    skope.write_pixel(dataset, 1, 0, 0, array_assigned_to_band_index_1[0, 0])
    skope.write_pixel(dataset, 1, 0, 1, array_assigned_to_band_index_1[0, 1])
    skope.write_pixel(dataset, 1, 1, 0, array_assigned_to_band_index_1[1, 0])
    skope.write_pixel(dataset, 1, 1, 1, array_assigned_to_band_index_1[1, 1])

    return dataset

# pylint: disable=redefined-outer-name, missing-docstring, line-too-long

def test_write_band_sets_assigns_expected_pixel_values(
        dataset: gdal.Dataset, array_assigned_to_band_index_0):
    assert np.array_equal(
        array_assigned_to_band_index_0,
        dataset.GetRasterBand(1).ReadAsArray()
    )

def test_write_pixel_sets_assigns_expected_pixel_values(
        dataset: gdal.Dataset, array_assigned_to_band_index_1):
    assert np.array_equal(
        array_assigned_to_band_index_1,
        dataset.GetRasterBand(2).ReadAsArray()
    )

def test_read_band_returns_expected_pixel_values(
        dataset: gdal.Dataset, array_assigned_to_band_index_0):
    assert np.array_equal(
        array_assigned_to_band_index_0,
        skope.read_band(dataset, 0)
    )

def test_read_pixel_returns_expected_pixel_values(
        dataset: gdal.Dataset, array_assigned_to_band_index_1):
    assert skope.read_pixel(dataset, 1, 0, 0) == array_assigned_to_band_index_1[0, 0]
    assert skope.read_pixel(dataset, 1, 0, 1) == array_assigned_to_band_index_1[0, 1]
    assert skope.read_pixel(dataset, 1, 1, 0) == array_assigned_to_band_index_1[1, 0]
    assert skope.read_pixel(dataset, 1, 1, 1) == array_assigned_to_band_index_1[1, 1]
