'''Abstractions for working with GDAL-compatible raster datasets.'''
import os
from typing import List, Tuple

import numpy
from osgeo import gdal
import skope

class RasterDataset:
    '''Class representing a GDAL-compatible raster dataset.'''
    @staticmethod
    def new(filename: str, file_format: str, pixel_type,
            rows: int, cols: int, bands: int,
            origin_long: float, origin_lat: float,
            pixel_width: float, pixel_height: float,
            coordinate_system='WGS84'):
        '''Create a new GDAL dataset, flush it to disk, and return a
        RasterDataset referencing it.'''
        skope.create_dataset(
            filename, file_format, pixel_type, rows, cols, bands, origin_long,
            origin_lat, pixel_width, pixel_height, coordinate_system
        )

        return RasterDataset(filename)

    def __init__(self, dataset):
        '''Initialize a RasterDataset either from gdal.Dataset object or a path
        to a GDAL-compatible raster dataset file.'''
        self.gdal_dataset, self.filename = _get_gdal_dataset_for_argument(dataset)
        self._geotransform = self.gdal_dataset.GetGeoTransform()
        self._affine = None
        self._inverse_affine = None
        self._array = self.gdal_dataset.ReadAsArray()

        # ensure that the latitudinal axis of the dataset points north
        if not self.geotransform[5] < 0:
            raise ValueError('The dataset ' + self.filename + ' is not northup')

    @property
    def bands(self) -> int:
        '''Return the number of bands in the raster dataset.'''
        return self.gdal_dataset.RasterCount

    @property
    def rows(self) -> int:
        '''Return the number of rows of pixels in the raster dataset.'''
        return self.gdal_dataset.RasterYSize

    @property
    def cols(self) -> int:
        '''Return the number of columns of pixels in the raster dataset.'''
        return self.gdal_dataset.RasterXSize

    @property
    def shape(self) -> Tuple[int]:
        '''Return the dimensions of the 3-D array of pixel values in the
        dataset as the 3-tuple (bands, rows columns).'''
        return self._array.shape

    @property
    def geotransform(self) -> List[float]:
        '''Return the six elements of the geotransform matrix of the dataset
        as a list.'''
        return self._geotransform

    @property
    def origin_long(self) -> float:
        '''Return the longitude of the northwest corner of the dataset coverage.'''
        return self.geotransform[0]

    @property
    def origin_lat(self) -> float:
        '''Return the latitude of the northwest corner of the dataset coverage.'''
        return self.geotransform[3]

    @property
    def origin(self) -> (float, float):
        '''Return a tuple representing the (longitude, latitude) coordinates of
        the northwest corner of the dataset coverage.'''
        return self.geotransform[0], self.geotransform[3]

    @property
    def pixel_size_x(self) -> float:
        '''Return the longitudinal dimensions of a pixel in degrees.'''
        return self.geotransform[1]

    @property
    def pixel_size_y(self) -> float:
        '''Return the latitudinal dimensions of a pixel in (positive) degrees.'''
        return -self.geotransform[5]

    @property
    def affine(self) -> List[float]:
        '''Return the affine matrix for the dataset.'''
        if self._affine is None:
            self._affine = skope.get_affine(self.gdal_dataset)
        return self._affine

    @property
    def inverse_affine(self) -> List[float]:
        '''Return the inverse affine matrix for the dataset.'''
        if self._inverse_affine is None:
            self._inverse_affine = ~self.affine # pylint: disable=invalid-unary-operand-type
        return self._inverse_affine

    @property
    def pixel_size(self) -> (float, float):
        '''Return a tuple representing the (longitudinal, latitudinal)
        dimensions of a pixel in degrees.'''
        return (self.pixel_size_x, self.pixel_size_y)

    @property
    def northwest_corner(self) -> (float, float):
        '''Return a tuple representing the (longitude, latitude) coordinates of
        the northwest (upper left) corner of the dataset coverage.'''
        return self.origin

    @property
    def northeast_corner(self) -> (float, float):
        '''Return a tuple representing the (longitude, latitude) coordinates of
        the northeast (upper right) corner of the dataset coverage.'''
        return self.affine * (self.cols, 0)

    @property
    def southeast_corner(self) -> (float, float):
        '''Return a tuple representing the (longitude, latitude) coordinates of
        the southeast (lower right) corner of the dataset coverage.'''
        return self.affine * (self.cols, self.rows)

    @property
    def southwest_corner(self) -> (float, float):
        '''Return a tuple representing the (longitude, latitude) coordinates of
        the southwest (lower left) corner of the dataset coverage.'''
        return self.affine * (0, self.rows)

    @property
    def center(self) -> (float, float):
        '''Return a tuple representing the (longitude, latitude) coordinates of
        the center of the dataset coverage.'''
        return self.affine * (self.cols/2, self.rows/2)

    def pixel_in_coverage(self, row: int, column: int) -> bool:
        '''Return true if the given indices refer to a pixel within the
        dataset coverage.'''
        return 0 <= column < self.cols and 0 <= row < self.rows

    def pixel_at_point(self, longitude: float, latitude: float) -> (int, int):
        '''Return the (row, column) indices of the pixel at the given geospatial
        coordinates if they are in the dataset coverage, and None otherwise.'''
        fractional_column, fractional_row = self.inverse_affine * (longitude, latitude)
        if self.pixel_in_coverage(fractional_row, fractional_column):
            return int(fractional_row), int(fractional_column)
        return None

    def value_at_pixel(self, band_index: int, row: int, column: int):
        '''Return the value of the pixel with the given (row, column) indices.'''
        return self._array[band_index, row, column]

    def value_at_point(self, longitude: float, latitude: float, band_index: int):
        '''Return the value of the pixel with the given (longitude, latitude)
        coordinates in the specified band.'''
        row, column = self.pixel_at_point(longitude, latitude)
        return self.value_at_pixel(band_index, row, column)

    def series_at_pixel(self, row: int, column: int, begin: int = None,
                        end: int = None) -> numpy.ndarray:
        '''Return the values of the pixels with the given (row, column) indices
        in the specified range of bands.'''
        if begin is None:
            begin = 0
        if end is None:
            end = self.bands
        series_length = end - begin
        series = numpy.empty(series_length)
        for series_index in range(series_length):
            series[series_index] = self._array[series_index + begin, row, column]
        return series

    def series_at_point(self, longitude: float, latitude: float,
                        begin: int = None, end: int = None) -> numpy.ndarray:
        '''Return the values of the pixels with the given (longitude, latitude)
        coordinates in the specified range of bands.'''
        row, column = self.pixel_at_point(longitude, latitude)
        return self.series_at_pixel(row, column, begin, end)

# Private helper methods

def _get_gdal_dataset_for_argument(dataset) -> (gdal.Dataset, str):
    '''Examine the dataset argument and return, as a tuple, the corresponding gdal.Dataset object
    and the path to the dataset file if known.'''

    # if the argument is a gdal.Dataset instance return it along with a null dataset path
    if isinstance(dataset, gdal.Dataset):
        gdal_dataset = dataset
        gdal_dataset_path = None

    # if the argument is a string, interpret it as the path to the datafile,
    # open the file with GDAL, and return the gdal.Dataset instance for it with the path
    elif isinstance(dataset, str):
        gdal_dataset_path = dataset
        if not os.path.isfile(gdal_dataset_path):
            raise FileNotFoundError('Dataset file not found at path ' + gdal_dataset_path)

        gdal_dataset = gdal.Open(gdal_dataset_path)
        if gdal_dataset is None:
            raise ValueError('Invalid dataset file found at path ' + gdal_dataset_path)

    # otherwise raise an argument TypeError exception
    else:
        raise TypeError('Expected a gdal.Dataset object or a string ' +
                        'representing the path to a datafile.')

    return  gdal_dataset, gdal_dataset_path
