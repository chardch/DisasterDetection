# THIS SCRIPT NEEDS PILLOW 4.3.0. IT WILL ERROR OUT ON 5.0.0
# RUN pip install Pillow==4.3.0 before running
import os
import sys
from PIL import Image

img_dir = '/host/datasets/AIRS/trainval/val/image'
length = 10240 # determined to prevent error of tiles outside image
print(img_dir)

for fname in os.listdir(img_dir):
    #print(os.path.join(root, name))
    if os.path.splitext(os.path.join(img_dir, fname))[1].lower() == ".tif":
        if os.path.isfile(os.path.splitext(os.path.join(img_dir, fname))[0] + ".jpg"):
            print("A jpeg file already exists for %s" % name)
            # If a jpeg is *NOT* present, create one from the tiff.
        else:
            outfile = os.path.splitext(os.path.join(img_dir + '_jpg_split', fname))[0] + ".jpg"
            print('outfile', outfile)
            try:
                im = Image.open(os.path.join(img_dir, fname))
                print("Generating jpeg for %s" % fname)
                im.thumbnail(im.size)
                im.size = (length, length)
                im.save(outfile, "JPEG", quality=100)
            except Exception: 
                print(sys.exc_info()[0])
print('done')
