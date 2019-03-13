import numpy as np
from PIL import Image
import geopandas as gpd
import os
import pandas as pd
import rasterio
import shapely
from shapely.geometry import box
import pandas as pd
from decimal import Decimal

# Keep CRS consistent, always use espg:4326
CRS = {'init':'epsg:4326'}

tiles_preevent_1 = '/host/datasets/maria/pre_event/20161214-20161125/tiles/'
tiles_preevent_2 = '/host/datasets/maria/pre_event/20170512-20170121/tiles/'
tiles_preevent_3 = '/host/datasets/maria/pre_event/20161031-20161021/tiles/'
harvey_tiles_dir = '/host/datasets/harvey/'
harvey_tiles_dirs = [harvey_tiles_dir + d for d in os.listdir(harvey_tiles_dir) if d.startswith('2017')]
harvey_tiles = [f for f in os.listdir(d) for d in harvey_tiles_dirs]
harvey_tiles = [d + '/' +  f for d in harvey_tiles_dirs for f in os.listdir(d)]
building_gjson = '/host/datasets/harvey/boundingboxes-all-damagearea-pixelcoords.shp'

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

#tiles_to_use = tiles_noaa
#tile_names = [tiles_to_use + f for f in os.listdir(tiles_to_use) if f.endswith('tif')]
df = pd.DataFrame(harvey_tiles)
df.columns = ['file_name']

df['bounds_lbrt'] = df['file_name'].apply(lambda x: get_bounds(x))
df['geometry'] = df['bounds_lbrt'].apply(lambda x: box(*x))
df['img_height_width'] = df['file_name'].apply(lambda x: get_image_height_width(x))
df['img_height'] = df['img_height_width'].apply(lambda x: x[0])
df['img_width'] = df['img_height_width'].apply(lambda x: x[1])

# Get the height and width to later use for converting the bounding boxes to image pixel positions
df['width'] = df['bounds_lbrt'].apply(lambda x: get_width(*x))
df['height'] = df['bounds_lbrt'].apply(lambda x: get_height(*x))
df['min_x'] = df['bounds_lbrt'].apply(lambda x: x[0])
df['min_y'] = df['bounds_lbrt'].apply(lambda x: x[1])

tiles_geo = gpd.GeoDataFrame(df, crs=CRS, geometry = df['geometry'])
buildings = gpd.read_file(building_gjson)
building_tiles = gpd.sjoin(tiles_geo, buildings, how="inner", op='intersects')

#building_tiles.to_crs(epsg=mercator_crs)
buildings['index_right'] = buildings.index
rejoined = building_tiles.merge(buildings, on = 'index_right')

# get the relation bounding boxes to the tile's top left point
min_x = rejoined['min_x'].apply(lambda x: Decimal(x))
min_y = rejoined['min_y'].apply(lambda x: Decimal(x))
rejoined['b_min_x'] = ((rejoined['geometry_y'].apply(lambda x: Decimal(x.bounds[0])) - min_x) / rejoined['width']).apply(lambda x: max(float(x), 0.0))
rejoined['b_min_y'] = ((rejoined['geometry_y'].apply(lambda x: Decimal(x.bounds[3])) - min_y) / rejoined['height']).apply(lambda x: max(1.0 - float(x), 0.0))
rejoined['b_max_x'] = ((rejoined['geometry_y'].apply(lambda x: Decimal(x.bounds[2])) - min_x) / rejoined['width']).apply(lambda x: min(float(x), 1.0))
rejoined['b_max_y'] = ((rejoined['geometry_y'].apply(lambda x: Decimal(x.bounds[1])) - min_y) / rejoined['height']).apply(lambda x: min(1.0 - float(x), 1.0))

rejoined['b_min_x'] = (rejoined['b_min_x'] * rejoined['img_width']).apply(lambda x: int(x))
rejoined['b_min_y'] = (rejoined['b_min_y'] * rejoined['img_height']).apply(lambda x: int(x))
rejoined['b_max_x'] = (rejoined['b_max_x'] * rejoined['img_width']).apply(lambda x: int(x))
rejoined['b_max_y'] = (rejoined['b_max_y'] * rejoined['img_height']).apply(lambda x: int(x))

def min__(x, bound):
    return min(x, bound)

def max__(x, bound):
    return max(x, bound)

margin = 20
filtered = rejoined
  # min is actually the max and vice ver
filtered['b_min_x'] = filtered['b_min_x'].apply(lambda x: max(x-margin,0))
filtered['b_max_y'] = filtered['b_max_y'].apply(lambda x: max(x-margin,0))
filtered['b_max_x'] = filtered['b_max_x'].apply(lambda x: x+margin)
filtered['b_max_x'] = filtered[['b_max_x', 'img_width']].apply(lambda x: min__(*x), axis=1)
filtered['b_min_y'] = filtered['b_min_y'].apply(lambda x: x +margin)
filtered['b_min_y'] = filtered[['b_min_y', 'img_height']].apply(lambda x: min__(*x), axis = 1)

filtered = filtered[['file_name', 'b_min_x', 'b_min_y', 'b_max_x', 'b_max_y']]
filtered['label'] = 'building'
filtered = filtered[(filtered['b_max_x'] - filtered['b_min_x']) * (filtered['b_max_y'] - filtered['b_min_y']) >= 200]
filtered.to_csv('/host/datasets/harvey/harvey_annotations_margin.csv', header = False, index = False)
# Possibly flatten the coordinates if the above isn't producing good results, since the earth is spherical, but don't foresee the issue since the tiles are so small that it's virtually linear
# mercator_crs=3395
# tiles_mercator = tiles_geo.to_crs(epsg=mercator_crs)
# buildings_mercator = buildings.to_crs(epsg=mercator_crs) 
