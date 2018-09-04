import skope.analysis as sa

from argparse import ArgumentParser

def main():

    parser = ArgumentParser()
    parser.add_argument("datafile", help="path to raster dataset file")
    parser.add_argument("x", type=int, help="x coordinate of point")
    parser.add_argument("y", type=int, help="y coordinate of point")
    args = parser.parse_args()
    
    raster_dataset = sa.RasterDataset(args.datafile)
    series = raster_dataset.series_at_pixel(0, 0)

    for value in series:
        print(value)

if __name__ == '__main__':
    main()