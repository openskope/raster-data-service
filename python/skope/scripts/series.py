'''Script for extracting a timeseries from a raster dataset.'''
from argparse import ArgumentParser

import skope

def main():
    '''Extract the timeseries defined by command-line arguments to the script.'''

    parser = ArgumentParser()
    parser.add_argument('-f', dest='datafile', help='path to raster dataset file')

    pixel_coord_group = parser.add_argument_group()
    pixel_coord_group.add_argument('-col', '-column', '-x',
                                   dest='pixel_column', type=int,
                                   help='column index of pixel to sample')
    pixel_coord_group.add_argument('-row', '-y', dest='pixel_row', type=int,
                                   help='row index of pixel to sample')

    geospatial_coord_group = parser.add_argument_group()
    geospatial_coord_group.add_argument('-longitude', '-long', '-lon',
                                        dest='longitude', type=float,
                                        help='longitude of point to sample')
    geospatial_coord_group.add_argument('-latitude', '-lat',
                                        dest='latitude', type=float,
                                        help='latitude of point to sample')

    args = parser.parse_args()
    print(args)

    if ((args.pixel_column is None) == (args.longitude is None)
            or (args.pixel_row is None) == (args.latitude is None)
            or (args.pixel_column is None) != (args.pixel_row is None)
            or (args.longitude is None) != (args.latitude is None)):
        parser.error('Provide either the indices of the pixel to sample using\n' +
                     'the -x and -y options, or the geospatial coordinates of\n' +
                     'the point to sample using the -lat and -long options.')

    raster_dataset = skope.RasterDataset(args.datafile)

    if args.pixel_column is not None:
        series = raster_dataset.series_at_pixel(row=args.pixel_row, column=args.pixel_column)
    else:
        series = raster_dataset.series_at_point(args.longitude, args.latitude)

    for value in series:
        print(value)

if __name__ == '__main__':
    main()
