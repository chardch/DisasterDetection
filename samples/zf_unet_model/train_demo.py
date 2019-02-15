import numpy as np
from zf_unet_224_model import ZF_UNET_224, dice_coef_loss, dice_coef, preprocess_input
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image

img_x = 224
img_y = 224
image_file = '/home/ubuntu/DeepDisaster/samples/zf_unet_model/input.jpg'
output_file = '/home/ubuntu/DeepDisaster/samples/zf_unet_model/result.jpg'
train_dir = '/host/datasets/AIRS/trainval/train'
train_image_dir = train_dir + '/image_jpg'
label_image_dir = train_dir + '/label_jpg'

train_base_dir = '/host/datasets/AIRS/trainval/train'
train_image_dir = train_base_dir + '/image_jpg/all_classes'
train_mask_dir = train_base_dir + 'label_jpg/all_classes'

def load_images_and_masks(image_dir, mask_dir):
    img_filenames = os.listdir(train_dir)

    train_data = np.asarray([open_and_resize(train_dir + '/' + f) for f in img_filenames])
    test_data = np.asarray([open_and_resize(label_dir + '/' + f) for f in img_filenames])
    return (images, masks)

def open_and_resize(image_file, x=img_x, y=img_y):
    img = Image.open(image_file)
    img_resized = img.resize((x, y), Image.ANTIALIAS)
    arr = np.array(img_resized) # should preprocess this first, with the meth


def main():
    model = ZF_UNET_224(weights='generator')
    optim = Adam()
    model.compile(optimizer=optim, loss=dice_coef_loss, metrics=[dice_coef])
    (images, masks) = load_images_and_masks(train_image_dir, train_mask_dir)
    #model.fit()

    #normalize the image pixel value to be between 0 and 1
    image_datagen = ImageDataGenerator(rescale=1./255)
    mask_datagen = ImageDataGenerator(rescale=1./255)
    image_generator = image_datagen.flow_from_directory(
        train_image_dir, 
        target_size = (224, 224),
        batch_size = 1,
        class_mode = None)

    mask_generator = mask_datagen.flow_from_directory(
        label_image_dir, 
        target_size = (224, 224),
        batch_size = 1,
        class_mode = None)
    
    train_generator = zip(image_generator, mask_generator)
    model.fit_generator(
        train_generator,
        steps_per_epoch=100,
        epochs=50)
    model.save('/host/Downloads/test_model.h5')
    

if __name__ == '__main__':
    main()
