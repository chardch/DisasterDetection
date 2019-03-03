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
building_gjson = '/host/datasets/maria/buildings.geojson'

def get_bounds(file_name, tiles_dir):
    tile = rasterio.open(tiles_dir + file_name)
    left, bottom, right, top = tile.bounds # confirm the orientation
    return (left, bottom, right, top)

def get_width(x_min, y_min, x_max, y_max):
    return Decimal(x_max) - Decimal(x_min)

def get_height(x_min, y_min, x_max, y_max):
    return Decimal(y_max) - Decimal(y_min)

tile_names = [f for f in os.listdir(tiles_preevent_1) if f.endswith('tif')]
df = pd.DataFrame(tile_names)
df.columns = ['file_name']

df['bounds_lbrt'] = df['file_name'].apply(lambda x: get_bounds(x, tiles_preevent_1))
df['geometry'] = df['bounds_lbrt'].apply(lambda x: box(*x))

# Get the height and width to later use for converting the bounding boxes to image pixel positions
df['width'] = df['bounds_lbrt'].apply(lambda x: get_width(*x))
df['height'] = df['bounds_lbrt'].apply(lambda x: get_height(*x))
df['min_x'] = df['bounds_lbrt'].apply(lambda x: x[0])
df['min_y'] = df['bounds_lbrt'].apply(lambda x: x[2])

tiles_geo = gpd.GeoDataFrame(df, crs=CRS, geometry = df['geometry'])
buildings = gpd.read_file(building_gjson)
building_tiles = gpd.sjoin(df, buildings, how="inner", op='intersects')
