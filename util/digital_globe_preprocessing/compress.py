"""
GDAL wrapper to compress GeoTIFFs given a compression method.
"""

import os
import argparse


def compress_tif(original_tif, compression_method="JPEG",
                 predictors=2, output_dir="compressed/"):
    """
    This function takes an uncompressed GeoTIFF and compresses it with one of
    four compression methods:

        - Packbits
        - JPEG
        - Deflate
        - LZW

    For LZW and Deflate, you can choose the number of predictors.

    :param original_tif: The uncompressed GeoTIFF to be compressed
    :param compression_method: Packbits, JPEG, Deflate, or LZW
    :param predictors: Default is 2
    :param output_dir: Name of directory in which to save compressed images
    :return: Creates a new compressed TIF in directory folder
    """

    new_tif_base = original_tif.split('.')[0]
    packbit_base = "_packbit_compressed.tif"
    jpeg_base = "_jpeg_compressed.tif"
    deflate_base = "_deflate_compressed.tif"
    lzw_base = "_lzw_compressed.tif"

    command_packbits = "gdal_translate -of GTiff-co COMPRESS=PACKBITS -co\
     TILED=YES " + original_tif + " " + new_tif_base + packbit_base
    command_jpeg = "gdal_translate -co COMPRESS=JPEG -co TILED=YES " + original_tif + " " + new_tif_base + jpeg_base
    command_deflate = "gdal_translate -of GTiff -co COMPRESS=DEFLATE -co\
     PREDICTOR=" + str(predictors) + " -co TILED=YES " + original_tif + " " + new_tif_base + deflate_base
    command_lzw = "gdal_translate -of GTiff -co COMPRESS=LZW -co PREDICTOR=" + str(predictors) + " -co TILED=YES " + original_tif + " " + new_tif_base + lzw_base

    command_mv = "mv " + new_tif_base

    if compression_method == "JPEG":
        os.system(command_jpeg)
        os.system(command_mv + jpeg_base + " " + output_dir)
    elif compression_method == "Packbits":
        os.system(command_packbits)
        os.system(command_mv + packbit_base + " " + output_dir)
    elif compression_method == "Deflate":
        os.system(command_deflate)
        os.system(command_mv + deflate_base + " " + output_dir)
    elif compression_method == "LZW":
        os.system(command_lzw)
        os.system(command_mv + lzw_base + " " + output_dir)


def compress_directory(input_dir, output_dir, compression_method="JPEG",
                       predictors=2):
    """
    Compresses directory of TIFFs.
    Compression methods are JPEG, Deflate, Packbits, or LZW.
    Predictors for Deflate and LZW are defaulted at 2.
    :param input_dir: Directory with uncompressed TIFFs
    :param output_dir: New directory for compressed TIFs
    :param compression_method: JPEG, Packbits, Deflate, or LZW
    :param predictors: Default is 2
    :return: A new directory populated with compressed TIFFs
    """

    if os.path.exists(output_dir) is False:
        os.mkdir(output_dir)
    else:
        pass

    for filename in os.listdir(input_dir):

        file = input_dir + "/" + filename
        compress_tif(file, compression_method, predictors, output_dir)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(epilog='Type in directory of TIFs with\
                                     this script in the parent directory.')
    parser.add_argument('input_dir', help='The directory that the TIFs are in')
    parser.add_argument('output_dir', help='Output directory for compressed TIFs')
    parser.add_argument('compression_method', default="JPEG")
    parser.add_argument('predictors', default=2)
    args = parser.parse_args()

    compress_directory(args.input_dir, args.output_dir, args.compression_method, args.predictors)
