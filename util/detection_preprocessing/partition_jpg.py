import os
import sys
from PIL import Image
from multiprocessing import Pool
import numpy as np

train_base = '/host/datasets/AIRS/trainval/train/'
train_img_dir = train_base + 'image_jpg'
train_label_dir = train_base + 'label_jpg'
img_out_dir = train_base + 'image_jpg_split_80'
label_out_dir = train_base + 'label_jpg_split_80'

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
    return split_arr(file, train_label_dir, label_out_dir)

def split_img(file):
    return split_arr(file, train_img_dir, img_out_dir)

def split_arr(file, in_path, out_path):
    try:
        im = Image.open(in_path + '/' + file)
        print("Generating jpeg for %s" % (in_path + '/' + file))
        im_arr = np.array(im)
        print(im_arr.shape)
        im_parts = partition_img(im_arr)
        for i in range(len(im_parts)):
            outfile = out_path + '/' + file.replace('_vis','').replace('.jpg','') + '_' + str(i) + ".jpg"
            if os.path.isfile(outfile):
                print('outfile exists: ', outfile)
                continue 
            print('outfile: ', outfile)
            img = Image.fromarray(im_parts[i])
            print("asdfasdfsadf")
            img.save(outfile, "JPEG", quality=60)
    except Exception as e: 
        print("error: " + str(e))

if __name__ == '__main__':
    image_names = os.listdir(train_img_dir)
    threads = 6
    for f in image_names:
        split_img(f)
        split_mask(f.replace('.jpg', '_vis.jpg'))
    #with Pool(threads) as p:
    #    images = p.map_async(split_img, image_names)
    #    images.wait()

    #with Pool(threads) as p:
    #    p.map(split_mask, image_names)

print('done')
