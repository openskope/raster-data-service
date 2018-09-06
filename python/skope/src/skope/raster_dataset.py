import affine
import numpy
import os
import osr
import skope

from osgeo import gdal
from typing import List, Tuple

################################################################################
# Class definition for RasterDataset
################################################################################

class RasterDataset:

    @staticmethod
    def new(filename: str, format: str, pixel_type, 
            rows: int, cols: int, bands: int, 
            origin_long: float, origin_lat: float,
            pixel_width: float, pixel_height: float, 
            coordinate_system='WGS84'):

        skope.create_dataset(
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
    def bands(self) -> int:
        return self.gdal_dataset.RasterCount

    @property
    def rows(self) -> int:
        return self.gdal_dataset.RasterYSize

    @property
    def cols(self) -> int:
        return self.gdal_dataset.RasterXSize

    @property
    def shape(self) -> Tuple[int]:
        return self._array.shape

    @property
    def geotransform(self) -> List[float]:
        return self._geotransform

    @property
    def origin_long(self) -> float:
        return self.geotransform[0]

    @property
    def origin_lat(self) -> float:
        return self.geotransform[3]

    @property
    def origin(self) -> (float, float):
        return self.geotransform[0], self.geotransform[3]

    @property
    def pixel_size_x(self) -> float:
        return self.geotransform[1]

    @property
    def pixel_size_y(self) -> float:
        return -self.geotransform[5]

    @property
    def affine(self) -> List[float]:
        if self._affine is None:
            self._affine = skope.get_affine(self.gdal_dataset)
        return self._affine

    @property
    def inverse_affine(self) -> List[float]:
        if self._inverse_affine is None:
            self._inverse_affine = ~self.affine
        return self._inverse_affine

    @property
    def pixel_size(self) -> float:
        return (self.geotransform[1], -self.geotransform[5])

    @property
    def northwest_corner(self) -> (float, float):
        return self.affine * (0,0)

    @property
    def northeast_corner(self) -> (float, float):
        return self.affine * (self.cols, 0)

    @property
    def southeast_corner(self) -> (float, float):
        return self.affine * (self.cols, self.rows)

    @property
    def southwest_corner(self) -> (float, float):
        return self.affine * (0, self.rows)

    @property
    def center(self) -> (float, float):
        return self.affine * (self.cols/2, self.rows/2)

    def pixel_in_coverage(self, row: int, column: int) -> bool:
        return (column >= 0 and column <= self.cols and
                row >= 0 and row <= self.rows)

    def pixel_at_point(self, longitude: float, latitude: float) -> (int, int):
        fractional_column, fractional_row = self.inverse_affine * (longitude, latitude)
        if self.pixel_in_coverage(fractional_row, fractional_column):
            row, column = int(fractional_row), int(fractional_column)
            return row, column
        else:
            return None

    def value_at_pixel(self, band_index: int, row: int, column: int):
        return self._array[band_index, row, column]

    def value_at_point(self, longitude: float, latitude: float, band_index: int):
        row, column = self.pixel_at_point(longitude, latitude)
        return self.value_at_pixel(band_index, row, column)

    def series_at_pixel(self, row: int, column: int, start: int = None, 
                        end: int = None) -> numpy.ndarray:
        if start is None:
            start = 0
        if end is None:
            end = self.bands
        series = numpy.empty(end - start)
        for series_index in range(len(series)):
            series[series_index] = self._array[series_index + start, row, column]
        return series

    def series_at_point(self, longitude: float, latitude: float, 
                        start: int = None, end: int = None) -> numpy.ndarray:
        row, column = self.pixel_at_point(longitude, latitude)
        return self.series_at_pixel(row, column, start, end)

################################################################################
# Private helper methods
################################################################################

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