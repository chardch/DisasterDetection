from zf_unet_224_model import ZF_UNET_224, dice_coef_loss, dice_coef, preprocess_input
from keras.optimizers import Adam
import numpy as np
from PIL import Image

img_x = 224
img_y = 224
image_file = '/home/ubuntu/DeepDisaster/samples/zf_unet_model/input.jpg'
output_file = '/home/ubuntu/DeepDisaster/samples/zf_unet_model/result.jpg'
def main():
    model = ZF_UNET_224(weights='generator')
    optim = Adam()
    model.compile(optimizer=optim, loss=dice_coef_loss, metrics=[dice_coef])

    img = Image.open(image_file)
    img_resized = img.resize((img_x, img_y), Image.ANTIALIAS)OB
    arr = np.array(img_resized) # should preprocess this first, with the meth

    batch_of_one = arr.reshape((1, img_x, img_y, 3))  # (num in batch, pixels x, pixels y, channels)
    output = model.predict(batch_of_one)
    output_img = Image.fromarray(output.reshape((img_x, img_y)).astype('uint8') * 255)
    output_img.save(output_file)

if __name__ == '__main__':
    main()