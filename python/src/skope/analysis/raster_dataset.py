import affine
import osr
import numpy as np
from osgeo import gdal
import skope.analysis

class RasterDataset:

    def __init__(self, 
                 filename, 
                 format, 
                 pixel_type, 
                 rows, 
                 cols, 
                 bands, 
                 origin_x, 
                 origin_y, 
                 pixel_width, 
                 pixel_height, 
                 coordinate_system='WGS84'):

        self.filename = filename
        self.row_count = rows
        self.column_count = cols
        self.band_count = bands
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.pixel_size_x = pixel_width
        self.pixel_size_y = pixel_height

        self.gdal_dataset = skope.analysis.create_dataset(
            self.filename, 
            format, 
            pixel_type,
            self.row_count,
            self.column_count, 
            self.band_count, 
            self.origin_x, 
            self.origin_y, 
            self.pixel_size_x, 
            self.pixel_size_y, 
            coordinate_system)
        
        self._affine = skope.analysis.get_affine(self.gdal_dataset)
        self._inverse_affine = ~self._affine


