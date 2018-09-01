import affine
import osr
import numpy as np
import os
from osgeo import gdal
import skope.analysis

################################################################################
# Class definition for RasterDataset
################################################################################

class RasterDataset:

    @staticmethod
    def new(filename, format, pixel_type, rows, cols, bands, origin_long, origin_lat,
            pixel_width, pixel_height, coordinate_system='WGS84'):

        skope.analysis.create_dataset(
            filename, format, pixel_type, rows, cols, bands, origin_long, origin_lat,
            pixel_width, pixel_height, coordinate_system
        )

        return RasterDataset(filename)

    def __init__(self, dataset):

        self.gdal_dataset, self.filename = _get_gdal_dataset_for_argument(dataset)
        self._geotransform = self.gdal_dataset.GetGeoTransform()
        self._affine = skope.analysis.get_affine(self.gdal_dataset)
        self._inverse_affine = ~self._affine

    @property
    def bands(self):
        return self.gdal_dataset.RasterCount

    @property
    def rows(self):
        return self.gdal_dataset.RasterYSize

    @property
    def cols(self):
        return self.gdal_dataset.RasterXSize

    @property
    def shape(self):
        return self.bands, self.rows, self.cols 

    @property
    def geotransform(self):
        return self._geotransform

    @property
    def origin_long(self):
        return self.geotransform[0]

    @property
    def origin_lat(self):
        return self.geotransform[3]

    @property
    def origin(self):
        return self.geotransform[0], self.geotransform[3]

    @property
    def pixel_size_x(self):
        return self.geotransform[1]

    @property
    def pixel_size_y(self):
        return -self.geotransform[5]

    @property
    def affine(self):
        return self._affine

    @property
    def inverse_affine(self):
        return self._inverse_affine

    @property
    def pixel_size(self):
        return (self.geotransform[1], -self.geotransform[5])

    @property
    def northwest_corner(self):
        return self.affine * (0,0)

    @property
    def northeast_corner(self):
        return self.affine * (self.cols, 0)

    @property
    def southeast_corner(self):
        return self.affine * (self.cols, self.rows)

    @property
    def southwest_corner(self):
        return self.affine * (0, self.rows)

    @property
    def center(self):
        return self.affine * (self.cols/2, self.rows/2)

    def pixel_in_coverage(self, pixel_x, pixel_y):
        return (pixel_x >= 0 and pixel_x <= self.cols and
                pixel_y >= 0 and pixel_y <= self.rows)

    def pixel_for(self, longitude, latitude):
        pixel_fractional_x, pixel_fractional_y = self.inverse_affine * (longitude, latitude)
        if self.pixel_in_coverage(pixel_fractional_x, pixel_fractional_y):
            return int(pixel_fractional_x), int(pixel_fractional_y)
        else:
            return None

    def read_pixel(self, row, column, band):
        selected_band = self.gdal_dataset.GetRasterBand(band)
        pixel_array = selected_band.ReadAsArray()
        return pixel_array[row, column]

    def read_pixel_at_point(self, longitude, latitude, band):
        pixel_x, pixel_y = self.pixel_for(longitude, latitude)
        return self.read_pixel(pixel_x, pixel_y, band)

################################################################################
# Private helper methods
################################################################################

def _get_gdal_dataset_for_argument(dataset):
    '''Examine the dataset argument and return, as a tuple, the corresponding gdal.Dataset object
    and the path to the dataset file if known.'''

    # if the argument is a gdal.Dataset instance return it along with a null dataset path
    if isinstance(dataset, gdal.Dataset):
        gdal_dataset = dataset
        gdal_dataset_path = None

    # if the argument is a string, interpret it as the path to the datafile,
    # open the file with GDAL, and return the gdal.Dataset instance for it with the path
    elif isinstance(dataset, str):

        if (not os.path.isfile(dataset)):
            raise FileNotFoundError('Dataset file not found at path ' + dataset)

        gdal_dataset_path =  dataset
        gdal_dataset = None
        try:
            gdal_dataset = gdal.Open(dataset)
        except:
            pass
        finally:
            if (gdal_dataset is None):
                raise ValueError('Invalid dataset file found at path ' + dataset)

    # otherwise raise an argument TypeError exception
    else:
        raise TypeError('Expected a gdal.Dataset object or a string representing the path to a datafile.')

    return  gdal_dataset, gdal_dataset_path