import numpy as np
from PIL import Image
from skimage import measure

def get_crops_from_image_arr(image_arr, binary_mask):
    """Get crops of connected components, based on binary_mask, from image_arr."""
    crops = []
    bboxes = get_bboxes(binary_mask)
    for row_start, col_start, row_end, col_end in bboxes:
        crop_arr = image_arr[row_start:row_end, col_start:col_end]
        crop = Image.fromarray(crop_arr)
        crops.append(crop)
    return crops

def get_bboxes(binary_mask, connectivity=1, pixel_threshold = 100):
    """
    binary_mask: binary 2-D array, representing pixels labelled as building = 1, otherwise = 0.
    connectivity: 1 - only counts vertical and horizontal connections. 2 - also counts diagonals.
    return: list of  minimum area bounding boxes for each connected component in image_arr.
    """
    labeled_connected_components = measure.label(binary_mask, connectivity=connectivity)
    regions = measure.regionprops(img_labeled)            
    return [region.bbox for region in regions if len(region.coords) < pixel_threshold]

