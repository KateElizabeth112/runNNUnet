import argparse
import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl

# argparse
parser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-r", "--root_dir", default=None, help="Root directory for nnUNet")
parser.add_argument("-t", "--task_id", default=None, help="ID of the task")

args = vars(parser.parse_args())

# set up variables
ROOT_DIR = args['root_dir']
TASK_ID = args['task_id']
NUM_CHANNELS = 2

# Check the predictions made by nnUNet - make plots and calculate Dice score
img_path = os.path.join(ROOT_DIR, "nnUNet_raw_data_base/nnUNet_raw_data/{}/imagesTs".format(TASK_ID))
label_path = os.path.join(ROOT_DIR, "nnUNet_raw_data_base/nnUNet_raw_data/{}/labelsTs".format(TASK_ID))
pred_path = os.path.join(ROOT_DIR, "inference/")
output_dir = os.path.join(ROOT_DIR, "predictions/")


def PlotSliceAndPrediction(image_slice, labels_slice, preds_slice, save_path=""):
    labels_slice[labels_slice > 1] = 1
    preds_slice[preds_slice > 1] = 1

    alpha_array_labels = np.zeros(labels_slice.shape)
    alpha_array_labels[labels_slice > 0] = 0.5

    alpha_array_preds = np.zeros(preds_slice.shape)
    alpha_array_preds[preds_slice > 0] = 0.5

    plt.subplot(121)
    plt.imshow(image_slice, cmap='gray')
    plt.imshow(labels_slice, cmap='jet', alpha=alpha_array_labels, vmin=0, vmax=2)
    plt.title('Ground Truth')

    plt.axis('off')

    plt.subplot(122)
    plt.imshow(image_slice, cmap='gray')
    plt.imshow(preds_slice, cmap='jet', alpha=alpha_array_preds, vmin=0, vmax=2)
    plt.title('Predictions')

    plt.axis('off')

    # Calculate Dice score
    dice = np.sum(preds_slice[labels_slice == 1]) * 2.0 / (np.sum(preds_slice) + np.sum(labels_slice))

    plt.suptitle("Dice score:  {0:.2f}".format(dice))

    if save_path == "":
        plt.show()
    else:
        plt.savefig(save_path)

    return dice


def main():
    files = os.listdir(img_path)
    ds_length = len(files)
    # create an empty array to store results
    dice_all = np.zeros((NUM_CHANNELS, ds_length))
    nsd_all = np.zeros((NUM_CHANNELS, ds_length))

    j = 0
    for f in files:
        # try to load the file and the label so we can visualise them
        if f.endswith(".nii.gz"):
            # extract the file name so we can also open the label file
            id = f.split('_')[1]
            label_name = "pancreas_" + id + ".nii.gz"
            print(label_name, f)

            img = nib.load(os.path.join(img_path, f)).get_fdata()
            lab = nib.load(os.path.join(label_path, label_name)).get_fdata()
            pred = nib.load(os.path.join(pred_path, label_name)).get_fdata()


            # Visualise
            dice = PlotSliceAndPrediction(np.rot90(img[:, :, 0]), np.rot90(lab[:, :, 0]),
                                          np.rot90(pred[:, :, 0]),
                                          save_path=os.path.join(output_dir, "pancreas_" + id + ".png"))

            dice_all[1, j] = dice

            j += 1

    # Save results
    f = open(os.path.join(output_dir, "results.pkl"), 'wb')
    pkl.dump([dice_all, nsd_all], f)
    f.close()


if __name__ == "__main__":
    main()