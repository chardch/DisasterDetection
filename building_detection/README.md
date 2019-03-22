# Building detection model

The implementation we are using is keras-retinanet. The other zf_unet_model and object_detection_api contain experiments that we didn't end up using.

# Goal

The goal of this portion of our framework is to detect buildings. The input is an RGB aerial image and the output is a list of building bounding boxes contains four coordinates, x,y of top left corner and x,y of the bottom right corner.
