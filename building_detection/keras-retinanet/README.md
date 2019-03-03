# RetinaNet model for building detection

This is the keras implementation of Retina Net from https://github.com/fizyr/keras-retinanet. To install, run `pip install . --user` in this repo and make sure you have `tensorflow` installed first.

The original implementation is trained on ImageNet, so we transfer learn on our processed dataset.
The current results are from the AIRS dataset, which contains 220k buildings across 13k images. The bounding boxes are in annotation_fixed.csv.

# Training on our dataset
Run `run_train.sh`, which will start training a RetinaNet with Resnet50 backbone previously trained on ImageNet, batch size of 16, resized images of 480 x 480, for 300 iterations, each with 500 steps.

# Results

Due to limitations on the training speed when using many images, currently the validation set has been using 9 images with 324 building instances. Each image has a variable number of buildings. They come from satellite imagery, which contains any number of buildings.

## Evaluation Metrics

After 20,500 steps of training:
Test set metrics with 1504 images

`26428 instances of class building with average precision: 0.7034`

`mAP: 0.7034`

Full progression of training results are in train.log

Sample output from earlier in the training process after about 7000 steps of training.

![bounding box prediction](example_output/drawn_bboxes.jpg?raw=true "Predicted building bounding boxes")