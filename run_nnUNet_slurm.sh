#!/bin/bash
# Example of running python script in a batch mode
#SBATCH -c 4 # Number of CPU Cores
#SBATCH -p gpushigh # Partition (queue)
#SBATCH --gres gpu:1 # gpu:n, where n = number of GPUs
#SBATCH --mem 20G # memory pool for all cores
#SBATCH --nodelist monal04 # SLURM node
#SBATCH --output=slurm.%N.%j.log # Standard output and error log

# Launch virtual environment
source venv/bin/activate

# Set environment variables
ROOT_DIR='/vol/biomedic3/kc2322/data/MSDPancreas_nnUNet/'
TASK='Task800'
DS='MSDPancreas'

export nnUNet_raw_data_base=$ROOT_DIR"nnUNet_raw_data_base"
export nnUNet_preprocessed=$ROOT_DIR"nnUNet_preprocessed"
export RESULTS_FOLDER=$ROOT_DIR"RESULTS_FOLDER"

echo $nnUNet_raw_data_base
echo $nnUNet_preprocessed
echo $RESULTS_FOLDER

# Run script to generate dataset json
#python3 generateDatasetJson.py -r $ROOT_DIR -n $DS -t $TASK

# Plan and preprocess data
nnUNet_plan_and_preprocess -t 800 --verify_dataset_integrity

# Train
nnUNet_train 2d nnUNetTrainerV2 Task800 0 --npz