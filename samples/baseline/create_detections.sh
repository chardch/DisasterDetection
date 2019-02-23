#!/bin/bash

TESTLIST="christchurch_519_14.jpg christchurch_519_15.jpg"

for i in $TESTLIST; do
    echo $i
    python3 create_detections.py -c ./transfer_model/export/Servo/1550789701/saved_model.pb  -o 'preds_output/'$i'_transfer.txt' '/host/datasets/AIRS/train/image_jpg_split/'$i
done
