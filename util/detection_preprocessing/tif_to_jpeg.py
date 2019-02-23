#Use the latest version of Pillow before running this
import os
import sys
from PIL import Image

#img_dir = '/host/datasets/AIRS/trainval/train/image'
length = 10240 # determined to prevent error of tiles outside image

def convert_tif_to_jpg(img_dir, fname):
  if os.path.splitext(os.path.join(img_dir, fname))[1].lower() == ".tif":
    if os.path.isfile(os.path.splitext(os.path.join(img_dir, fname))[0] + ".jpg"):
      print("A jpeg file already exists for %s" % name)
      # If a jpeg is *NOT* present, create one from the tiff.
    else:
      outfile = os.path.splitext(os.path.join(img_dir + '_jpg', fname))[0] + ".jpg"
      print('outfile', outfile)
      try:
        im = Image.open(os.path.join(img_dir, fname))
        print("Generating jpeg for %s" % fname)
        #im.thumbnail(im.size)
        im.size = (length, length)
        im.save(outfile, "JPEG", quality=100)
      except Exception: 
        print(sys.exc_info()[0])

if __name__ == '__main__':
  img_dir = sys.argv[1]
  print(img_dir)
  fnames = os.listdir(img_dir)
  [convert_tif_to_jpg(img_dir, f) for f in fnames]
  print('done')
