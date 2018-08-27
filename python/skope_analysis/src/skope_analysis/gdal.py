import osr
import numpy as np
from osgeo import gdal

def create_dataset(filename, format, pixel_type, 
                   rows, cols, bands, 
                   origin_x, origin_y, 
                   pixel_width, pixel_height, 
                   coordinate_system='WGS84'):
    '''Create a new GDAL dataset and datafile, returning the dataset object.'''
    # get the GDAL driver for the specified data format
    driver = gdal.GetDriverByName(format)

    # create the a new gdal.Dataset instance and corresponding data file
    dataset = driver.Create(filename, cols, rows, bands, pixel_type)
    
    # set the spatial dimensions, resolution, and orientation of the dataset
    dataset.SetGeoTransform((origin_x, pixel_width, 0, origin_y, 0, -pixel_height))

    # set the geospatial projection and coordinate system for the dataset
    srs = osr.SpatialReference()
    srs.SetWellKnownGeogCS(coordinate_system)
    dataset.SetProjection(srs.ExportToWkt())
    
    # return the gdal.Dataset object corresponding to the open datafile
    return dataset

def open_dataset(filename):
    '''Open an existing dataset file with GDAL and return a gdal.Dataset object.'''
    return gdal.Open(filename)

def write_band(dataset, band, array, nodata):
    '''Copy a 2D numpy array to the specified band of a gdal.Dataset.'''
    selected_band = dataset.GetRasterBand(band)
    selected_band.WriteArray(array)
    selected_band.SetNoDataValue(nodata)
    selected_band.FlushCache()
    
def read_pixel(dataset, band, row, column):
    '''Read one pixel of a gdal.Dataset.'''
    selected_band = dataset.GetRasterBand(band)
    pixel_array = selected_band.ReadAsArray()
    return pixel_array[row, column]
    
def write_pixel(dataset, band, row, column, value):
    '''Write value to one pixel of a gdal.Dataset.'''
    selected_band = dataset.GetRasterBand(band)
    array = selected_band.ReadAsArray()
    array[row, column] = value
    selected_band.WriteArray(array)
    selected_band.FlushCache()
