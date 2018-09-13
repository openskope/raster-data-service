'''Tests of the RasterDataset coordinate properties and methods.'''
import pytest

import numpy as np
from osgeo import gdal

from skope import RasterDataset

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
                   array_assigned_to_band_index_1) -> RasterDataset:
    '''Create a new dataset, and set its values using write_band()
    functions.'''

    datafile_path = test_dataset_filename(__file__)

    raster_dataset = RasterDataset.create(datafile_path, 'GTiff',
                                          gdal.GDT_Float32,
                                          shape=(2, 2, 2),
                                          origin=(-123, 45),
                                          pixel_size=(1.0, 1.0),
                                          coordinate_system='WGS84')

    # set the values in bands 0 and 1 with calls to write_band
    raster_dataset.write_band(0, array_assigned_to_band_index_0, float('nan'))
    raster_dataset.write_band(1, array_assigned_to_band_index_1, float('nan'))

    raster_dataset.flush()

    return raster_dataset

# pylint: disable=redefined-outer-name, missing-docstring, line-too-long

def test_value_at_pixel_returns_value_of_each_pixel_in_dataset(raster_dataset: RasterDataset):
    assert raster_dataset.value_at_pixel(band_index=0, row=0, column=0) == 1
    assert raster_dataset.value_at_pixel(band_index=0, row=0, column=1) == 2
    assert raster_dataset.value_at_pixel(band_index=0, row=1, column=0) == 3
    assert raster_dataset.value_at_pixel(band_index=0, row=1, column=1) == 4
    assert raster_dataset.value_at_pixel(band_index=1, row=0, column=0) == 11
    assert raster_dataset.value_at_pixel(band_index=1, row=0, column=1) == 12
    assert raster_dataset.value_at_pixel(band_index=1, row=1, column=0) == 13
    assert raster_dataset.value_at_pixel(band_index=1, row=1, column=1) == 14

def test_value_at_point_returns_value_at_0_0_for_origin(raster_dataset: RasterDataset):
    assert raster_dataset.value_at_point(-123, 45, band_index=0) == 1
    assert raster_dataset.value_at_point(-123, 45, band_index=1) == 11

def test_value_at_point_returns_value_at_1_1_near_southeast_corner(raster_dataset: RasterDataset):
    assert raster_dataset.value_at_point(-121.001, 43.001, band_index=0) == 4
    assert raster_dataset.value_at_point(-121.001, 43.001, band_index=1) == 14
