"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import tensorflow as tf
import numpy as np

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict
from convert_mask_to_bbox import get_bboxes_xy, get_bboxes_from_contours

flags = tf.app.flags
flags.DEFINE_string('mask_dir', '', 'Path to the mask input')
flags.DEFINE_string('image_dir', '', 'Path to images')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'Building':
        return 1
    else:
        None

def create_tf_example(filename, image_path, mask_path):
    with tf.gfile.GFile(os.path.join(image_path, '{}'.format(filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    #encoded_jpg_io = io.BytesIO(encoded_jpg)
    try:
        im = Image.open(mask_path + '/' + filename)

    except Exception as e:
        print("error: " + str(e))
        return None

    print("Generating bounding box for %s" % (mask_path + '/' + filename))
    im_arr = np.array(im)
    height, width = im_arr.shape
    bboxes = get_bboxes_from_contours(im_arr) # (y_min, x_min, y_max, x_max)

    filename = filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []
    # referenced from https://github.com/DIUx-xView/baseline/blob/master/xview_class_labels.txt
    class_name = 'Building'.encode('utf8')
    class_num = 1
    for bbox in bboxes:
        y_min, x_min, y_max, x_max = bbox
        print('bbox: ', str(y_min/width), str(x_min/width), str(y_max/width), str(x_max/width))
        xmins.append(x_min/width)
        ymins.append(y_min/height)
        xmaxs.append(x_max/width)
        ymaxs.append(y_max/height)
        classes_text.append(class_name)
        classes.append(class_num)

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example

def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    image_dir = os.path.join(FLAGS.image_dir)
    masks_dir = os.path.join(FLAGS.mask_dir)
    mask_filenames = os.listdir(masks_dir)
    for mask_fname in mask_filenames:
        tf_example = create_tf_example(mask_fname, image_dir, masks_dir)
        if tf_example is not None:
            writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
