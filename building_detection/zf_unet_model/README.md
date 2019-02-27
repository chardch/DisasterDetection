# Example of using to a modified unet from https://github.com/ZFTurbo/ZF_UNET_224_Pretrained_Model
Predict man-made feature segmentation on an image. This model got 2nd place on the Kaggle DSTL competition, https://www.kaggle.com/c/dstl-satellite-imagery-feature-detection.

Ran this on using this docker image: https://hub.docker.com/r/waleedka/modern-deep-learning/
Command to start up this image: docker run -it -p 8888:8888 -p 6006:6006 -v ~/:/host waleedka/modern-deep-learning

## Model input and output format:
input: 224 x 224 x number of channels (defined by INPUT_CHANNELS, I used 3 for rgb image, e.g. numpy array of shape (224,224,3))

output: binary mask of 224 x 224 x 1, where 1 is defined by OUTPUT_MASK_CHANNELS and in the case of 1 appears to correspond to the pixel being segmented as manmade feature, such as a road or home. TODO: Will verify, since only tested on damaged image atm.

training labels format: segmentation mask, such as 2-D binary array 
## Further use cases for this
We could use this directly. However, we could also take the pretrained weights (or completely retrain) and do some further training on labelled damaged buildings to fine tune the weights for our use case on damaged man made features.

## Script to run through a demo: demo.py (needs changes)
