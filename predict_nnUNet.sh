#!/bin/bash

# Launch virtual environment
source venv/bin/activate

# Set environment variables
export nnUNet_raw_data_base="nnUNet_raw_data_base"
export nnUNet_preprocessed="nnUNet_preprocessed"
export RESULTS_FOLDER="RESULTS_FOLDER"

# Define variables
ROOT_DIR='/vol/biomedic3/kc2322/data/MSDPancreas_nnUNet/'
TASK='Task800'
DS='MSDPancreas'

INPUT_DIR=$ROOT_DIR"nnUNet_raw_data_base/nnUNet_raw_data/"$TASK"/imagesTs"
OUTPUT_DIR=$ROOT_DIR"inference"

# make predictions
nnUNet_predict -i $INPUT_DIR -o $OUTPUT_DIR -t $TASK -m 2d -chk model_best

# check predictions and make plots
python3 checkPredictions.py -r $ROOT_DIR -t $TASK