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

        # expose key metadata as public attributes
        self.rows = self.gdal_dataset.RasterYSize
        self.cols = self.gdal_dataset.RasterXSize
        self.bands = self.gdal_dataset.RasterCount
        self.geotransform = self.gdal_dataset.GetGeoTransform()
        self.origin_long = self.geotransform[0]
        self.origin_lat = self.geotransform[3]
        self.pixel_size_x = self.geotransform[1]
        self.pixel_size_y = -self.geotransform[5]
        self.affine = skope.analysis.get_affine(self.gdal_dataset)
        self.inverse_affine = ~self.affine

    def pixel_in_coverage(self, pixel_x, pixel_y):
        return (pixel_x >= 0 and pixel_x <= self.cols and
                pixel_y >= 0 and pixel_y <= self.rows)

    def pixel_for(self, longitude, latitude):
        pixel_fractional_x, pixel_fractional_y = self.inverse_affine * (longitude, latitude)
        if self.pixel_in_coverage(pixel_fractional_x, pixel_fractional_y):
            return int(pixel_fractional_x), int(pixel_fractional_y)
        else:
            return None

    def pixel_size(self):
        return (self.pixel_size_x, self.pixel_size_y)

    def origin(self):
        return self.northwest_corner()

    def northwest_corner(self):
        return self.affine * (0,0)

    def northeast_corner(self):
        return self.affine * (self.cols, 0)

    def southeast_corner(self):
        return self.affine * (self.cols, self.rows)

    def southwest_corner(self):
        return self.affine * (0, self.rows)

    def center(self):
        return self.affine * (self.cols/2, self.rows/2)


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