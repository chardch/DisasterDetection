import os
import sys
from PIL import Image
from multiprocessing import Pool
import numpy as np

train_base = '/host/datasets/AIRS/trainval/train/'
train_img_dir = train_base + 'image_jpg/all_classes'
train_label_dir = train_base + 'label_jpg/all_classes'

#length = 10240
def partition_img(im, length=10240, nrows=4, ncols=4):
    (rows, cols) = im.shape[0:2]
    row_size = int(rows / nrows)
    col_size = int(cols / ncols)
    imgs = []
    channels = len(im.shape)
    for i in range(nrows):
        for j in range(ncols):
            if channels == 3:
                img = im[row_size * i: row_size * (i+1)-1, col_size*j:col_size*(j+1)-1,:]
            if channels == 2:
                img = im[row_size * i: row_size * (i+1)-1, col_size*j:col_size*(j+1)-1]
            imgs.append(img)
    print(len(imgs))
    return imgs

def split_mask(file):
    return split_arr(file, train_label_dir)

def split_img(file):
    return split_arr(file, train_img_dir)

def split_arr(file, path):
    try:
        im = Image.open(train_label_dir + '/' + file)
        print("Generating jpeg for %s" % (train_label_dir + '/' + file))
        #im.thumbnail(im.size)
        #im.size = (10000, 10000)
        im_arr = np.array(im)
        print(im_arr.shape)
        im_parts = partition_img(im_arr)
        print('hi')
        for i in range(len(im_parts)):
            outfile = '/host/datasets/AIRS/train_jpg_split/label/' + file.replace('.jpg','') + '_' + str(i) + ".jpg"
            print('outfile', outfile)
            img = Image.fromarray(im_parts[i])
            print("asdfasdfsadf")
            img.save(outfile, "JPEG", quality=100)
    except Exception as e: 
        print("error: " + str(e))

if __name__ == '__main__':
    image_names = os.listdir(train_img_dir)
    with Pool(4) as p:
        p.map(split_img, image_names)

#    with Pool(4) as p:
#        p.map(split_mask, image_names)

print('done')
