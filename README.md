# Video content classifier
An InceptionV3 CNN is daisy-chained to an LSTM RNN in order to classify videos into one of 6 categories:

1. Safe
1. Violence
1. Gun
1. Cold_Arms
1. Smoking
1. Kissing

## Requirements

This code requires you have Keras 2 and TensorFlow 1 or greater installed. Please see the `requirements.txt` file. To ensure you're up to date, run:

`pip install -r requirements.txt`

You must also have `ffmpeg` installed in order to extract the video files. If `ffmpeg` isn't in your system path (ie. `which ffmpeg` doesn't return its path, or you're on an OS other than *nix), you'll need to update the path to `ffmpeg` in `data/2_extract_files.py`.

## Getting the data

First, ensure the following file is present in the  from UCF into the `data` folder:

`cd data && wget http://crcv.ucf.edu/data/UCF101/UCF101.rar`

Then extract it with `unrar e UCF101.rar`.

Next, create folders (still in the data folder) with `mkdir train && mkdir test && mkdir sequences && mkdir checkpoints`.

Now you can run the scripts in the data folder to move the videos to the appropriate place, extract their frames and make the CSV file the rest of the code references. You need to run these in order. Example:

`python 1_move_files.py`

`python 2_extract_files.py`

## Extracting features

 On my Dell with a GeFore 960m GPU, this takes about 8 hours. If you want to limit to just the first N classes, you can set that option in the file.

## Training models

The Inception CNN is trained first using the `train_cnn.py` scipt.

Before you can run the `LSTM` , you need to extract features from the images with the CNN. This is done by running `extract_features.py`.

The LSTM is trained using the `train.py`script.

The LSTM is defined in `models.py`. Reference that file to see the model you are training in `train.py`.

Training logs are saved to CSV and also to TensorBoard files. To see progress while training, run `tensorboard --logdir=data/logs` from the project root folder.

## Demo/Using models




## Dataset Citation



