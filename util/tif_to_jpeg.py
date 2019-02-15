import os
import sys
from PIL import Image

img_dir = '/host/datasets/AIRS/trainval/train/image'
length = 10240 # determined to prevent error of tiles outside image
print(img_dir)
for root, dirs, files in os.walk(img_dir, topdown=False):
    for name in files:
        print(os.path.join(root, name))
        if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
            if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
                print("A jpeg file already exists for %s" % name)
            # If a jpeg is *NOT* present, create one from the tiff.
            else:
                outfile = os.path.splitext(os.path.join(img_dir + '_jpg_small', name))[0] + ".jpg"
                print('outfile', outfile)
                try:
                    im = Image.open(os.path.join(img_dir, name))
                    print("Generating jpeg for %s" % name)
                    im.thumbnail(im.size)
                    im.size = (length, length)
                    im.save(outfile, "JPEG", quality=100)
                except Exception: 
                    print(sys.exc_info()[0])
print('done')
