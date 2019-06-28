import csv
import numpy as np
import random
import glob
import os
import os.path
import sys
import operator
import threading
from processor import process_image
from keras.utils import to_categorical
from keras.models import load_model, Model
from keras.preprocessing import image
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.layers import Input
from subprocess import call
from tqdm import tqdm
from extractor import Extractor

class threadsafe_iterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return next(self.iterator)

def threadsafe_generator(func):
    """Decorator"""
    def gen(*a, **kw):
        return threadsafe_iterator(func(*a, **kw))
    return gen

class DataSet():
    """Class for managing our data."""

    def __init__(self, seq_length=80, class_limit=None, image_shape=(224, 224, 3)):
        """Constructor.
        seq_length = (int) the number of frames to consider
        class_limit = (int) number of classes to limit the data to.
            None = no limit.
        """
        self.seq_length = seq_length
        self.class_limit = class_limit
        self.sequence_path = os.path.join('data', 'demo_sequences')
        
        self.max_frames = 8000  # max number of frames a video can have for us to use it

        # Get the data.
        self.data = self.get_data()

        # Get the classes.
        self.classes = self.get_classes()

        # Now do some minor data cleaning.
        self.data = self.clean_data()

        self.image_shape = image_shape

    @staticmethod
    def get_data():
        """Load our data from file."""
        with open(os.path.join('data', 'demo_file.csv'), 'r') as fin:
            reader = csv.reader(fin)
            data = list(reader)

        return data

    def clean_data(self):
        """Limit samples to greater than the sequence length and fewer
        than N frames. Also limit it to classes we want to use."""
        data_clean = []
        for item in self.data:
            if int(item[2]) >= self.seq_length and int(item[2]) <= self.max_frames:# and item[1] in self.classes:
                data_clean.append(item)

        return data_clean

    def get_classes(self):
        """Extract the classes from our data. If we want to limit them,
        only return the classes we need."""

        # Sort them.
        classes = ['Safe','Violence','Gun','Cold_Arms','Smoking','Kissing']
        classes = sorted(classes)

        # Return.
        if self.class_limit is not None:
            return classes[:self.class_limit]
        else:
            return classes

    def get_extracted_sequence(self, data_type, sample):
        """Get the saved extracted features."""
        filename = sample[1]
        path = os.path.join(self.sequence_path, filename + '-' + str(self.seq_length) + \
            '-' + data_type + '.npy')
        if os.path.isfile(path):
            return np.load(path)
        else:
            return None

    def get_frames_by_filename(self, filename, data_type):
        """Given a filename for one of our samples, return the data
        the model needs to make predictions."""
        # First, find the sample row.
        sample = None

        for row in self.data:
            if row[1] == filename:
                sample = row
                break
        if sample is None:
            raise ValueError("Couldn't find sample: %s" % filename)

        # Get the sequence from disk.
        sequence = self.get_extracted_sequence(data_type, sample)
        if sequence is None:
            raise ValueError("Can't find sequence. Did you generate them?")
            
        return sequence

    @staticmethod
    def get_frames_for_sample(sample):
        """Given a sample row from the data file, get all the corresponding frame
        filenames."""
        path = os.path.join('data', sample[0])
        filename = sample[1]
        images = sorted(glob.glob(os.path.join(path, filename + '*jpg')))
        return images

    @staticmethod
    def rescale_list(input_list, size):
        """Given a list and a size, return a rescaled/samples list. For example,
        if we want a list of size 5 and we have a list of size 25, return a new
        list of size five which is every 5th element of the origina list."""
        assert len(input_list) >= size

        # Get the number to skip between iterations.
        skip = len(input_list) // size

        # Build our new output.
        output = [input_list[i] for i in range(0, len(input_list), skip)]

        # Cut off the last one if needed.
        return output[:size]

    def print_class_from_prediction(self, predictions, nb_to_return=6):
        """Given a prediction, print the top classes."""
        # Get the prediction for each label.
        label_predictions = {}
        for i, label in enumerate(self.classes):
            label_predictions[label] = predictions[i]

        # Now sort them.
        sorted_lps = sorted(
            label_predictions.items(),
            key=operator.itemgetter(1),
            reverse=True
        )

        # And return the top N.
        for i, class_prediction in enumerate(sorted_lps):
            if i > nb_to_return - 1 or class_prediction[1] == 0.0:
                break
            print("%s: %.2f" % (class_prediction[0], class_prediction[1]))

#------------------------------------------------------------------------------------------------------------------------------------1

def extract_files():
    os.chdir('./data')
    data_file = []
    folder_x = ['demo']
    for folder in folder_x:
        class_files = glob.glob(os.path.join(folder,'*.avi'))

    for video_path in class_files:
        # Get the parts of the file.
        video_parts = get_video_parts(video_path)

        train_or_test, filename_no_ext, filename= video_parts

        # Only extract if we haven't done it yet. Otherwise, just get
        # the info.
        if not check_already_extracted(video_parts):
            # Now extract it.
            src = os.path.join(train_or_test, filename)
            dest = os.path.join('demo_frames',filename_no_ext + '-%04d.jpg')
            call(["ffmpeg","-loglevel","error","-i",src, dest])

        # Now get how many frames it is.
        nb_frames = get_nb_frames_for_video(video_parts)

        data_file.append(['demo_frames', filename_no_ext, nb_frames])

        print("Generated %d frames for %s" % (nb_frames, filename_no_ext))

    with open('demo_file.csv', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(data_file)

    print("Extracted and wrote %d video files." % (len(data_file)))
    os.chdir('..')

def get_nb_frames_for_video(video_parts):
    """Given video parts of an (assumed) already extracted video, return
    the number of frames that were extracted."""
    train_or_test, filename_no_ext, _ = video_parts
    generated_files = glob.glob(os.path.join('demo_frames',
                                filename_no_ext + '*.jpg'))
    return len(generated_files)

def get_video_parts(video_path):
    """Given a full path to a video, return its parts."""
    parts = video_path.split(os.path.sep)
    filename = parts[1]
    filename_no_ext = filename.split('.')[0]
    train_or_test = parts[0]

    return train_or_test, filename_no_ext, filename

def check_already_extracted(video_parts):
    """Check to see if we created the -0001 frame of this file."""
    train_or_test, filename_no_ext, _ = video_parts
    return bool(os.path.exists(os.path.join('demo_frames',
                               filename_no_ext + '-0001.jpg')))

#------------------------------------------------------------------------------------------------------------------------------------2
"""
This generates extracted features for each video, which other
models make use of.
"""
def xtract_f(model_f=None, seq_length = 80):
    
    # Set defaults.
    class_limit = None  # Number of classes to extract. Can be 1-101 or None for all.

    # Get the dataset.
    data = DataSet(seq_length=seq_length, class_limit=class_limit)

    # get the model.
    if model_f is None:
        model = Extractor()
    else:
        model = Extractor(weights=os.path.join('data','checkpoints',model_f))

    #Loop through data.
    pbar = tqdm(total=len(data.data))
    for video in data.data:
        # Get the path to the sequence for this video.
        path = os.path.join('data', 'demo_sequences', video[1] + '-' + str(seq_length) + \
            '-features')  # numpy will auto-append .npy

        # Check if we already have it.
        if os.path.isfile(path + '.npy'):
            pbar.update(1)
            continue

        # Get the frames for this video.
        frames = data.get_frames_for_sample(video)

        # Now downsample to just the ones we need.
        frames = data.rescale_list(frames, seq_length)

        # Now loop through and extract features to build the sequence.
        sequence = []
        for image in frames:
            features = model.extract(image)
            sequence.append(features)

        # Save the sequence.
        np.save(path, sequence)
        pbar.update(1)
    pbar.close()
#------------------------------------------------------------------------------------------------------------------------------------3
"""
Given a video path and a saved model (checkpoint), produce classification
predictions.

The InceptionV3 pipelined to the LSTM model requires that features be extracted first before invoking this function.
"""
def predict(data_type, seq_length, saved_model, image_shape, video_name, class_limit):
    
    model = load_model(os.path.join('data','checkpoints',saved_model))

    # Get the data and process it.
    data = DataSet(seq_length=seq_length, class_limit=class_limit)
    
    # Extract the sample from the data.
    sample = data.get_frames_by_filename(video_name, data_type)

    # Predict!
    prediction = model.predict(np.expand_dims(sample, axis=0))
    print(" ")
    print("===============================================================")
    print(video_name)
    print("===============================================================")
    data.print_class_from_prediction(np.squeeze(prediction, axis=0))
#------------------------------------------------------------------------------------------------------------------------------------4
def main():
    print("Extracting files")
    extract_files()
    print("Extracted files")
    print("....................................................................................")
    print("Extracting features")
    xtract_f(cnn_model, seq_length=seq_length)
    print("Extracted features")
    print(" ")
    model = 'lstm'

    # Limit must match that used during training.
    class_limit = None
    
    data_type = 'features'
    image_shape = None

    os.chdir('data')
    folder_d = ['demo']
    for folder in folder_d:
        class_files = glob.glob(os.path.join(folder, '*.avi'))
    os.chdir('..')
    
    print("***************************************************************")
    print("Classifying videos now")
    print("***************************************************************")

    for video_path in class_files:
        # Get the parts of the file.
        video_parts = get_video_parts(video_path)        
        train_or_test, filename_no_ext, _ = video_parts
        predict(data_type, seq_length, rnn_model, image_shape, filename_no_ext, class_limit)
#------------------------------------------------------------------------------------------------------------------------------------5
#Main execution below, change weights file below if necessary
if __name__ == '__main__':
    
    # Sequence length must match the lengh used during training.
    seq_length = 60

    # Must be weight files.
    cnn_model = 'inception.023-0.76.hdf5'    #InceptionV3 model
    rnn_model = 'lstm-features.001-0.596.hdf5'    #LSTM model
    
    main()
