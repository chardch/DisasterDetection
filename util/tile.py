"""
GDAL wrapper to tile GeoTIFFs.
"""

import argparse
import logging
import os


def tile_tiff(tiff_file, output_dir, tile_size):
    logging.info("Tiling file {}".format(tiff_file))
    csv_out = "tile_georef_info.csv"
    cmd = "gdal_retile.py -v -r bilinear -levels 1 -ps {0} {0} -co\
     TILED=YES -co COMPRESS=JPEG -csv {1} -targetDir {2} {3}".format(tile_size, csv_out, output_dir, tiff_file)

    if not os.path.exists(output_dir):
        # Create the output directory and georef info csv file.
        logging.info("Creating output dir {}".format(output_dir))
        os.system("mkdir " + output_dir)

    os.system(cmd)


def tile_directory(directory, output_dir, tile_size):
    logging.info("Tiling dir {}".format(directory))
    for file in os.listdir(directory):
        tile_tiff(directory + "/" + file, output_dir, tile_size)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog='')
    parser.add_argument('input_tiff', help="GeoTIFFs to tile, can be a single file or a directory.")
    parser.add_argument('output_dir', help="Output dir in which to save tiles. Must be different than input dir.")
    parser.add_argument('tile_size', default=20000)

    args = parser.parse_args()
    tiff = args.input_tiff

    if os.path.isfile(tiff):
        tile_tiff(tiff, args.output_dir, args.tile_size)
    elif os.path.isdir(tiff):
        tile_directory(tiff, args.output_dir, args.tile_size)
    else:
        logging.info("input_tiff not a valid file or directory")
