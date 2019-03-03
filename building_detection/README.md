# Building detection model

The implementation we are using is keras-retinanet

# Bounding boxes

annotations_fixed.csv contains the bounding boxes for the processed AIRS dataset, which is not loaded here due to size constraints. 
The format of the file is `filename, min_x, min_y, max_x, max_y, class_name`.
