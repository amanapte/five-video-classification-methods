# Video content classifier
An InceptionV3 CNN is daisy-chained to an LSTM RNN in order to classify videos into one of 6 categories:

1. Safe
1. Violence
1. Gun
1. Cold_Arms
1. Smoking
1. Kissing

### A `.ipynb` file is also included which takes care of training the models. It can be used exclusivly to get the weight files but must be used along with Google Drive if using Google Colab.

## Requirements

This code requires you have Keras 2 and TensorFlow 1 or greater installed. Please see the `requirements.txt` file. To ensure you're up to date, run:

`pip install -r requirements.txt`  
`apt install gpac`  
`pip install tqdm`  

You must also have `ffmpeg` installed in order to extract the video files. If `ffmpeg` isn't in your system path (ie. `which ffmpeg` doesn't return its path, or you're on an OS other than *nix), you'll need to update the path to `ffmpeg` in `data/extract_files.py`.

## Getting the data

Download the datasets from:  
http://mvig.sjtu.edu.cn/research/adha/download.html  
https://www.kaggle.com/mohamedmustafa/real-life-violence-situations-dataset  
http://kt.agh.edu.pl/~grega/guns/

Next, create folders (still in the data folder) with:  
`mkdir train && mkdir test && mkdir sequences && mkdir checkpoints`  
`cd ./test/ && mkdir Safe Violence Gun Cold_Arms Smoking Kissing`  
`cd ./train/ && mkdir Safe Violence Gun Cold_Arms Smoking Kissing`  

And move the contents of the specified directories from the ADHA dataset into the `train` directories:
### Safe
brush_hair  
pour  
pick  
dive  
talk  
shake_hands  
hug  
climb_stairs  
stand  
pullup  
wave  
chew  
sit  
eat  
walk  
clap  
drink  
run  
### Violence
punch  
hit  
### Gun
shoot_gun  
### Cold_Arms
sword  
sword_exercise  
draw_sword  
### Smoking
smoke  
### Kissing
kiss  

Now you can run the script in the data folder to extract frames from the videos and make the CSV file for the rest of the code references.  
`python extract_files.py`

## Training models

The Inception CNN is trained first using the `train_cnn.py` scipt.

Before you can run the `LSTM` , you need to extract features from the images with the CNN. This is done by running `extract_features.py`.

The LSTM is trained using the `train.py`script.

The LSTM is defined in `models.py`. Reference that file to see the model you are training in `train.py`.

Training logs are saved to CSV and also to TensorBoard files. To see progress while training, run `tensorboard --logdir=data/logs` from the project root folder.

## Demo/Using models
First place the videos that are to be classified into the `demo` directory present int the `data` directory. After ensuring the appropriate weight files are set in the `demo.py` script run it.

## Dataset Citation

### Action clips dataset
Pang, Bo, Kaiwen Zha, and Cewu Lu. "Human Action Adverb Recognition: ADHA Dataset and A Three-Stream Hybrid Model." Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshops. 2018.
http://mvig.sjtu.edu.cn/research/adha/download.html

### Violence clips dataset
Real Life Violence Situations Dataset  
https://www.kaggle.com/mohamedmustafa/real-life-violence-situations-dataset

### Gun clips dataset
Grega, Michał, Seweryn Łach, and Radosław Sieradzki. "Automated recognition of firearms in surveillance video." 2013 IEEE International Multi-Disciplinary Conference on Cognitive Methods in Situation Awareness and Decision Support (CogSIMA). IEEE, 2013 .  
http://kt.agh.edu.pl/~grega/guns/
