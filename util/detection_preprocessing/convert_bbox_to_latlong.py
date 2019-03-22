import numpy as np
from PIL import Image
import geopandas as gpd
import os
import pandas as pd
import rasterio
import shapely
from shapely.geometry import box
import sys
import pandas as pd
from decimal import Decimal

# Given an image and bounding box, return the coordinates of the bounding box in lat long
# Take the image and get it's top left corner. Then calculate the percentage of image's pixel height and width
# the bounding box coordinates are at
# x_prop = x / pixel_width
# Then convert that to geo
# lat_offset = lat_width * x_prop
# lat_bbox_x = left + lat_offset

# longitude goes the opposite direction. increasing coordinates means further away from equator
def convert_image_coord_to_latlong(image_path, min_x, min_y, max_x, max_y):
  (left, bottom, right, top) = get_bounds(image_path)
  lat_width = right - left
  long_height = top - bottom
  (pixel_height, pixel_width) = get_image_height_width(image_path)
  min_x_offset = min_x / pixel_width
  min_y_offset = min_y / pixel_height
  max_x_offset = max_x / pixel_width
  max_y_offset = max_y / pixel_height
  min_x_lat_offset = lat_width * min_x_offset
  min_y_long_offset = long_height * min_y_offset
  max_x_lat_offset = lat_width * max_x_offset
  max_y_long_offset = long_height * max_y_offset
  min_x_lat = left + min_x_lat_offset
  min_y_long = top - min_y_long_offset
  max_x_lat = left + max_x_lat_offset
  max_y_long = top - max_y_long_offset
  # lat_left, lon_bot, lat_right, lon_top
  return (min_x_lat, min_y_long, max_x_lat, max_y_long)

# lon_bot < lon_top, even though pixel coordinates are opposite of this
def convert_latlong_to_img_coord(image_path, lat_left, lon_bot, lat_right, lon_top, margin = 15, threshold = 200):
  (left, bottom, right, top) = get_bounds(image_path)
  lat_width = right - left
  long_height = top - bottom
  (pixel_height, pixel_width) = get_image_height_width(image_path)
  x_min_pixel_offset = (lat_left - left) / lat_width * pixel_width
  y_min_pixel_offset = (top - lon_top) / long_height * pixel_height
  x_max_pixel_offset = (lat_right - left) / lat_width * pixel_width
  y_max_pixel_offset = (top - lon_bot) / long_height * pixel_height
  if (x_max_pixel_offset - x_min_pixel_offset) * (y_max_pixel_offset - y_min_pixel_offset) > 200:
    x_min = max(0, x_min_pixel_offset - margin)
    y_min = max(0, y_min_pixel_offset - margin)
    x_max = max(0, x_max_pixel_offset + margin)
    y_max = max(0, y_max_pixel_offset + margin)
    return (x_min_pixel_offset, y_min_pixel_offset, x_max_pixel_offset, y_max_pixel_offset)

def add_margin(image_path, x_min, y_min, x_max, y_max, margin = 15, threshold = 200):
  (pixel_height, pixel_width) = get_image_height_width(image_path)
  x_min = max(0, x_min - margin)
  y_min = max(0, x_min - margin)
  x_max = min(pixel_width, x_min + margin)
  y_max = min(pixel_height, x_min + margin)


def get_bounds(file_name, tiles_dir=None):
    if tiles_dir is not None:
        tile = rasterio.open(tiles_dir + file_name)
    else:
        tile = rasterio.open(file_name)
    left, bottom, right, top = tile.bounds # confirm the orientation
    return (left, bottom, right, top)

def get_width(x_min, y_min, x_max, y_max):
    return Decimal(x_max) - Decimal(x_min)

def get_height(x_min, y_min, x_max, y_max):
    return Decimal(y_max) - Decimal(y_min)

def get_image_height_width(file_name):
    im = Image.open(file_name)
    width, height = im.size
    return (height, width)

def main():
  file_to_convert = sys.argv[1]
  output_file = sys.argv[2]
  print(file_to_convert)
  print(output_file)
  with open(output_file, 'w') as f_out:
    with open(file_to_convert) as f:
      boxes = f.readlines()
      for box in boxes:
        image_path, x_min, y_min, x_max, y_max = box.split(',')
        geo_coords = convert_image_coord_to_latlong(image_path, float(x_min), float(y_min), float(x_max), float(y_max))
        f_out.write(image_path + ',' + str(geo_coords).replace(' ','').replace('(','').replace(')','') + '\n')

if __name__ == '__main__':
  main()
