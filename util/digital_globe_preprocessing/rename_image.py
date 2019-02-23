"""
Sometimes, multiple images from DigitalGlobe have the same filename. This is usually due to roughly the same area being
photographed on different days. We want to keep all images, in case some have cloud cover in certain areas that the
others don't.
"""

import argparse
import os


def rename_files(input_dir):
    fname_counter = 0

    for file in os.listdir(input_dir):
        f = input_dir + "/" + file
        if not file.endswith('tif'):
            split_f = file.split('.')
            new_f = "{0}/renamed/{1}_{2}.tif".format(input_dir, split_f[0], split_f[-1])
            os.system("mv {} {}".format(f, new_f))
            fname_counter += 1

    print("Renamed {} tiffs".format(fname_counter))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog='')
    parser.add_argument('input_dir', help="Dir including GeoTIFFs")

    args = parser.parse_args()

    rename_files(args.input_dir)
