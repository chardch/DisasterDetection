# RetinaNet model for building detection

This is the keras implementation of Retina Net from https://github.com/fizyr/keras-retinanet. To install, run `pip install . --user` in this repo and make sure you have `tensorflow` installed first.

The original implementation is trained on ImageNet, so we transfer learn on our processed dataset.
The current results are from the AIRS dataset, which contains 220k buildings across 13k images. The bounding boxes are in annotation_fixed.csv.

# Training on our dataset

Run `run_noaa.sh`, which will start training a RetinaNet with Resnet101 backbone previously trained on ImageNet, updating the entire network, with a learning rate of 0.0001, batch size of 2, and resize the images to 480 x 480.


# Results

We found that the best performing algorithm for the building detection was a RetinaNet with ResNet101 backbone, learning rate of 0.0001, achieving a mAP@0.25 of 0.743 and mAP@0.5 of 0.493.

![bounding box prediction](example_output/detection_output.png?raw=true "Predicted building bounding boxes")
