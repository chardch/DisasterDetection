# Script to generate annotations for bounding boxes in an image
# format:
# path/to/image.jpg,xmin,ymin,xmax,ymax,class_name
# if no bboxes: path/to/image.jpg,,,,,
# One annotation per line in fine csv. Images with multiple boxes should have multiple lines, one bounding box on each
from convert_mask_to_bbox import get_bboxes_xy
from PIL import Image
import numpy as np
import os
import sys

def generate_annotations(in_path, out_path):
    """
    in_path: path to directory of mask labels
    out_path: path to annotation output file
    """
    masks = os.listdir(in_path)
    with open(out_path, 'w') as f:
        for mask in masks:
            mask_path = in_path + '/' + mask
            img = Image.open(mask_path)
            img_arr = np.array(img)
            bboxes = get_bboxes_xy(img_arr)
            if len(bboxes) == 0:
                f.write('{},,,,,\n'.format(mask_path))
            else:
                for x_min, y_min, x_max, y_max in bboxes:
                    f.write('{},{},{},{},{},building\n'.format(mask_path, x_min, y_min, x_max, y_max))

if __name__ == '__main__':
    mask_dir = sys.argv[1]
    annotation_path = sys.argv[2]
    generate_annotations(mask_dir, annotation_path)
