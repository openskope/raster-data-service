import affine
import osr
import numpy as np
import os
from osgeo import gdal
import skope.analysis

def get_gdal_dataset_for_argument(dataset):
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

class RasterDataset:

    @staticmethod
    def new(filename, format, pixel_type, rows, cols, bands, origin_x, origin_y,
            pixel_width, pixel_height, coordinate_system='WGS84'):

        skope.analysis.create_dataset(
            filename, format, pixel_type, rows, cols, bands, origin_x, origin_y,
            pixel_width, pixel_height, coordinate_system
        )

        return RasterDataset(filename)

    def __init__(self, dataset):

        self.gdal_dataset, self.filename = get_gdal_dataset_for_argument(dataset)

        # expose key metadata as public attributes
        self.row_count = self.gdal_dataset.RasterYSize
        self.column_count = self.gdal_dataset.RasterXSize
        self.band_count = self.gdal_dataset.RasterCount
        self.geotransform = self.gdal_dataset.GetGeoTransform()
        self.origin_x = self.geotransform[0]
        self.origin_y = self.geotransform[3]
        self.pixel_size_x = self.geotransform[1]
        self.pixel_size_y = -self.geotransform[5]

        # assign internal attributes
        self._affine = skope.analysis.get_affine(self.gdal_dataset)
        self._inverse_affine = ~self._affine
