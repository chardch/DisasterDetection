import numpy as np
from PIL import Image
from skimage import measure

def get_bboxes_center_width_height(mask, connectivity = 1, pixel_threshold = 50):
    """
    mask: 2-D array, representing pixels labelled as building = 255, otherwise = 0.
    connectivity: 1 - only counts vertical and horizontal connections. 2 - also counts diagonals.
    return: list of bounding boxes (with small margin) for each connected component in mask.
    """
    x_len, y_len = mask.shape
    regions = get_regions(mask, connectivity)
    return [convert_topleft_bottomright_to_center_hw(region.bbox, x_len, y_len) 
            for region in regions if len(region.coords) > pixel_threshold]
    
def get_regions(mask, connectivity = 1):
    labeled_connected_components = measure.label(mask, connectivity=connectivity)
    return measure.regionprops(labeled_connected_components)

def convert_topleft_bottomright_to_center_hw(bbox, x_len, y_len, margin = 10):
    """ bbox_4tuple: 4 tuple of (x, y for top left point and x, y for bottom right point). """
    x_left, y_top, x_right, y_bottom = bbox
    x_left = max(x_left - margin, 0)
    y_top = max(y_top - margin, 0)
    x_right = min(x_right + margin, x_len-1)
    y_bottom = min(y_bottom + margin, y_len-1)

    center_x = int(np.floor((x_left + x_right) / 2))
    center_y = int(np.floor((y_top + y_bottom) / 2))
    width = x_right - x_left
    height = y_bottom - y_top
    return (center_x, center_y, width, height)


if __name__ == '__main__':
    
