#!/bin/bash

TESTLIST="christchurch_519_14.jpg christchurch_519_15.jpg"

for i in $TESTLIST; do
    echo $i
    python3 create_detections.py -c ../exported_transfer_v2/frozen_inference_graph.pb -o 'preds_output/'$i'.txt' '/host/datasets/AIRS/trainval/train/image_jpg_split/'$i
done
