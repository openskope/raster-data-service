import affine
import osr
import numpy as np
import os
from osgeo import gdal
import skope.analysis

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

        # if the constructor argument is a gdal.Dataset instance simply store it
        if isinstance(dataset, gdal.Dataset):
            self.filename = None
            self.gdal_dataset = dataset

        # if the argument is a string, interpret it as the path to the datafile,
        # open the file with GDAL, and store the gdal.Dataset instance for it
        elif isinstance(dataset, str):

            if (not os.path.isfile(dataset)):
                raise FileNotFoundError('Dataset file not found at path ' + dataset)

            self.gdal_dataset = None
            try:
                self.gdal_dataset = gdal.Open(dataset)
            except:
                pass

            if (self.gdal_dataset is None):
                raise ValueError('Invalid dataset file found at path ' + dataset)

            self.filename = dataset
        # otherwise raise an exception
        else:
            raise TypeError('Expected a gdal.Dataset object or a string representing the path to a datafile.')

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
