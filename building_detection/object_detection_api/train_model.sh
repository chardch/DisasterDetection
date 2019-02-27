#!/bin/bash
#Run this first if missing object detection library: 'export PYTHONPATH=$PYTHONPATH:/host/models/research:/host/models/research/slim'
PIPELINE_CONFIG_PATH=/host/DisasterDetection/building_detection/object_detection_api/model/multires/multires_building.config
MODEL_DIR=/host/DisasterDetection/building_detection/object_detection_api/transfer_model
NUM_TRAIN_STEPS=5
SAMPLE_1_OF_N_EVAL_EXAMPLES=1

python3 /host/DisasterDetection/samples/baseline/model_main.py \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --model_dir=${MODEL_DIR} \
    --num_train_steps=${NUM_TRAIN_STEPS} \
    --sample_1_of_n_eval_examples=$SAMPLE_1_OF_N_EVAL_EXAMPLES \
    --alsologtostderr