"""
Filters empty rasters. Useful after tiling; many tiles will result in blank rasters.
"""

import numpy as np
from osgeo import gdal
import argparse
import os


def is_raster_empty(tif_file):
    raster = gdal.Open(tif_file)
    raster_band = raster.GetRasterBand(1)
    band_array = np.array(raster_band.ReadAsArray())

    return np.max(band_array) < 1


def delete_file(file):
    command = "rm %s" % file
    os.system(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='Directory containing TIFs')
    args = parser.parse_args()

    input_dir = args.input_dir

    empty_rasters, ok_rasters = 0, 0
    num_files = 0
    for filename in os.listdir(input_dir):
        f = input_dir + "/" + filename
        if f.endswith(".tif") and is_raster_empty(f):
            empty_rasters += 1
            delete_file(f)
        else:
            ok_rasters += 1
            continue

        num_files += 1
        if num_files % 1000 == 0:
            print("Processed {} tiles...".format(str(num_files)))

    print ("Kept {} files".format(str(ok_rasters)))
    print("Deleted {} files".format(str(empty_rasters)))
