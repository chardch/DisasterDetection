# Utilities for building detection

`tif_to_jpg.py` converts tif to jpg.

`partition_jpg.py` splits a jpg image into smaller tiles. Ex. 10240 x 10240 image into 16 2560 x 2560 images.

`convert_mask_to_bbox.py` converts segmentation masks into bounding boxes with a margin.

`generate_csv_annotations.py` generates bounding boxes in the format to be used as annotations for the keras-retinanet model.

`crop.py` crops out bounding boxes from a given image.