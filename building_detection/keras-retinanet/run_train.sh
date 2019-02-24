#!/bin/bash
keras_retinanet/bin/train.py --backbone=resnet50 --image-min-side=400  --batch-size=8 --steps=100 --epochs=10 --tensorboard-dir=/host/DisasterDetection/building_detection/keras-retinanet/tfboard csv /host/datasets/AIRS/trainval/train/annotations.csv /host/datasets/AIRS/class_map.csv --val-annotations=/host/datasets/AIRS/trainval/val/annotations.csv
