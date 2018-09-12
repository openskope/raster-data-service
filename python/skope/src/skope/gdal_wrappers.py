'''Functions simplifying and standardizing access to GDAL libraries.'''
from typing import List

import affine
import numpy
import osr
from osgeo import gdal

def create_dataset(
        filename: str,
        file_format: str,
        pixel_type,
        bands: int,
        rows: int,
        columns: int,
        origin_long: float,
        origin_lat: float,
        pixel_width: float,
        pixel_height: float,
        coordinate_system='WGS84') -> gdal.Dataset:
    '''Create a new GDAL dataset and datafile, returning the dataset object.'''

    # get the GDAL driver for the specified dataset file format
    driver = gdal.GetDriverByName(file_format)

    # create the a new gdal.Dataset instance and corresponding data file
    gdal_dataset = driver.Create(filename, columns, rows, bands, pixel_type)

    # set the spatial dimensions, resolution, and orientation of the dataset
    gdal_dataset.SetGeoTransform((origin_long, pixel_width, 0, origin_lat, 0, -pixel_height))

    # set the geospatial projection and coordinate system for the dataset
    srs = osr.SpatialReference()
    srs.SetWellKnownGeogCS(coordinate_system)
    gdal_dataset.SetProjection(srs.ExportToWkt())

    # return the gdal.Dataset object corresponding to the open datafile
    return gdal_dataset

def open_dataset(filename: str) -> gdal.Dataset:
    '''Open an existing dataset file with GDAL and return a gdal.Dataset object.'''
    return gdal.Open(filename)

def read_band(gdal_dataset: gdal.Dataset, band_index: int) -> numpy.ndarray:
    '''Return pixel values of one band of a gdal.Dataset as a 2D numpy array.'''
    band_number = band_index + 1
    selected_band = gdal_dataset.GetRasterBand(band_number)
    return selected_band.ReadAsArray()

def write_band(gdal_dataset: gdal.Dataset, band_index: int, array: numpy.ndarray, nodata) -> None:
    '''Copy a 2D numpy array to the specified band of a gdal.Dataset.'''
    band_number = band_index + 1
    selected_band = gdal_dataset.GetRasterBand(band_number)
    selected_band.WriteArray(array)
    selected_band.SetNoDataValue(nodata)
    selected_band.FlushCache()

def read_pixel(gdal_dataset: gdal.Dataset, band_index: int, row: int, column: int) -> numpy.ndarray:
    '''Read one pixel of a gdal.Dataset.'''
    band_number = band_index + 1
    selected_band = gdal_dataset.GetRasterBand(band_number)
    pixel_array = selected_band.ReadAsArray()
    return pixel_array[row, column]

def write_pixel(gdal_dataset: gdal.Dataset, band_index: int, row: int, column: int, value) -> None:
    '''Write value to one pixel of a gdal.Dataset.'''
    band_number = band_index + 1
    selected_band = gdal_dataset.GetRasterBand(band_number)
    array = selected_band.ReadAsArray()
    array[row, column] = value
    selected_band.WriteArray(array)
    selected_band.FlushCache()

def get_affine(gdal_dataset: gdal.Dataset) -> List[float]:
    '''Return affine matrix for the dataset.'''
    geotransform = gdal_dataset.GetGeoTransform()
    return affine.Affine.from_gdal(geotransform[0], geotransform[1],
                                   geotransform[2], geotransform[3],
                                   geotransform[4], geotransform[5])
