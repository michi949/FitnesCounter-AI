"""@package retrain
"""

import os
import pickle
import random

import cv2
import numpy as np
from tqdm import tqdm

# Collect all pictures from the folders, resize it and then label it with the right folder name
DATADIR = "../data/classif"
CATEGORIES = ["push_up_down", "push_up_up", "squat_down", "squat_up"]
IMG_SIZE = 224

training_data = []


def create_training_data():
    """
    Reads the images from the classification dir and saves them as numpy array with their labels.
    """
    for category in CATEGORIES:  # do dogs and cats

        path = os.path.join(DATADIR, category)  # create path to dogs and cats
        class_num = CATEGORIES.index(category)  # get the classification  (0 or a 1). 0=dog 1=cat

        for img in tqdm(os.listdir(path)):  # iterate over each image per dogs and cats
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)  # convert to array
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
                training_data.append([new_array, class_num])  # add this to our training_data
            except Exception as e:  # in the interest in keeping the output clean...
                pass


def main():
    create_training_data()

    print(len(training_data))

    # mix the training data because one half would be cats the other dogs and not random
    random.shuffle(training_data)

    # x and y are input parameters. x = image data y = label data
    X = []
    y = []

    # label the images
    for features, label in training_data:
        X.append(features)
        y.append(label)

    X = np.array(X)

    # safe the data
    pickle_out = open("X.pickle", "wb")
    pickle.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open("y.pickle", "wb")
    pickle.dump(y, pickle_out)
    pickle_out.close()


if __name__ == "__main__":
    main()
