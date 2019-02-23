import numpy as np
from zf_unet_224_model import ZF_UNET_224, dice_coef_loss, dice_coef, preprocess_input
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import os

img_x = 224
img_y = 224
train_dir = '/host/DisasterDetection/datasets/AIRS/train'
train_image_dir = train_dir + '/image'
train_mask_dir = train_dir + '/label'

def load_images_and_masks(image_dir, mask_dir):
    img_filenames = os.listdir(train_image_dir)[0:4]
    print(len(img_filenames))
    images = np.asarray([open_and_resize(image_dir + '/' + f) for f in img_filenames])
    print('loaded train')
    masks = np.asarray([open_and_resize(mask_dir + '/' + f) for f in img_filenames])
    print('loaded mask')
    return (images, masks.reshape(masks.shape[0], masks.shape[1], masks.shape[2], 1))

def open_and_resize(image_file, x=img_x, y=img_y):
    img = Image.open(image_file)
    img_resized = img.resize((x, y), Image.ANTIALIAS)
    arr = np.array(img_resized)
    # arr = (arr - np.mean(arr)) / (np.std(arr) + 1e-8)
    arr = arr / 255
    return arr


def main():
    (images, masks) = load_images_and_masks(train_image_dir, train_mask_dir)
    model = ZF_UNET_224(img_x, img_y)
    #for layer in model.layers[:-2]:
    #    layer.trainable = False
    optim = Adam()

    #model.compile(optimizer=optim, loss=dice_coef_loss, metrics=[dice_coef])
    model.compile(optimizer=optim, loss='binary_crossentropy', metrics=['accuracy'])

    print(images.shape)
    print(masks.shape)
    model.fit(images, masks, epochs=100)

#    image_datagen = ImageDataGenerator(rescale=1./255)
#    mask_datagen = ImageDataGenerator(rescale=1./255)
#    image_generator = image_datagen.flow_from_directory(
#        train_image_dir, 
#        target_size = (224, 224),
#        batch_size = 1,
#        class_mode = None)
#
#    mask_generator = mask_datagen.flow_from_directory(
#        label_image_dir, 
#        target_size = (224, 224),
#        batch_size = 1,
#        class_mode = None)
#    
#    train_generator = zip(image_generator, mask_generator)
#    model.fit_generator(
#        train_generator,
#        steps_per_epoch=100,
#        epochs=50)
    model.save('/host/DisasterDetection/test_zf_unet_model_trained1.h5')
    

if __name__ == '__main__':
    main()
