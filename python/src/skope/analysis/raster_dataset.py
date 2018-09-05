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
        self._affine = None
        self._inverse_affine = None
        self._array = self.gdal_dataset.ReadAsArray()

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
        return self._array.shape

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
        if self._affine is None:
            self._affine = skope.analysis.get_affine(self.gdal_dataset)
        return self._affine

    @property
    def inverse_affine(self):
        if self._inverse_affine is None:
            self._inverse_affine = ~self.affine
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

    def pixel_in_coverage(self, pixel_row, pixel_column):
        return (pixel_column >= 0 and pixel_column <= self.cols and
                pixel_row >= 0 and pixel_row <= self.rows)

    def pixel_at_point(self, longitude, latitude):
        fractional_column, fractional_row = self.inverse_affine * (longitude, latitude)
        if self.pixel_in_coverage(fractional_row, fractional_column):
            row, column = int(fractional_row), int(fractional_column)
            return row, column
        else:
            return None

    def value_at_pixel(self, band, row, column):
        return self._array[band-1, row, column]

    def value_at_point(self, longitude, latitude, band):
        row, column = self.pixel_at_point(longitude, latitude)
        return self.value_at_pixel(band, row, column)

    def series_at_pixel(self, row, column):
        series = np.empty(self.bands)
        for band in range(0, self.bands):
            series[band] = self._array[band, row, column]
        return series

    def series_at_point(self, longitude, latitude):
        row, column = self.pixel_at_point(longitude, latitude)
        return self.series_at_pixel(row, column)

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