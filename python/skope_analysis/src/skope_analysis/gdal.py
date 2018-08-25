import osr
import numpy as np
from osgeo import gdal

def create_dataset_file(filename, format, pixel_type, 
                        rows, cols, bands, 
                        origin_x, origin_y, 
                        pixel_width, pixel_height, 
                        coordinate_system='WGS84'):

    # create the data set
    driver = gdal.GetDriverByName(format)
    dataset = driver.Create(filename, cols, rows, bands, pixel_type)
    
    # specify the data set dimensions and geospatial project projection
    dataset.SetGeoTransform((origin_x, pixel_width, 0, origin_y, 0, -pixel_height))
    srs = osr.SpatialReference()
    srs.SetWellKnownGeogCS(coordinate_system)
    dataset.SetProjection(srs.ExportToWkt())
    
    return dataset

def write_band(dataset, band, array, nodata):
    selected_band = dataset.GetRasterBand(band)
    selected_band.WriteArray(array)
    selected_band.SetNoDataValue(nodata)
    selected_band.FlushCache()
    
def read_pixel(dataset, band, row, column):
    selected_band = dataset.GetRasterBand(band)
    pixel_array = selected_band.ReadAsArray()
    return pixel_array[row, column]
    
def write_pixel(dataset, band, row, column, value):
    selected_band = dataset.GetRasterBand(band)
    array = selected_band.ReadAsArray()
    array[row, column] = value
    selected_band.WriteArray(array)
    selected_band.FlushCache()
    
   