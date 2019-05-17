import os
import pickle
import random

import cv2
import numpy as np
from tqdm import tqdm

# Collect all Pictures from the Folders, Resize it and then Label it with the right Folder Name
# So a pic in the folder Dog gets the Label Dog and the Number 0, Cat = 1



DATADIR = "C:/Users/reder/PycharmProjects/pro3/pythonmodel/data/classif/"
CATEGORIES = ["push_up_up", "push_up_down", "squat_up", "squat_down"]
#C:\Users\reder\PycharmProjects\pro3\pythonmodel\data\classif\push_up_up

IMG_SIZE = 224

training_data = []


# Sort the data, not the best way because with the piplining it would be way faster
def create_training_data():
    for category in CATEGORIES:

        path = os.path.join(DATADIR, category)  # create path to dogs and cats
        class_num = CATEGORIES.index(category)  # get the classification  (0 or a 1). 0=push_up_up 1=push_up_down

        for img in tqdm(os.listdir(path)):  # iterate over each image per dogs and cats
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)  # convert to array
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
                training_data.append([new_array, class_num])  # add this to our training_data
            except Exception as e:  # in the interest in keeping the output clean...
                pass
            # except OSError as e:
            #    print("OSErrroBad img most likely", e, os.path.join(path,img))
            # except Exception as e:
            #    print("general exception", e, os.path.join(path,img))


create_training_data()

print(len(training_data))

# mix the training data because one half would be cats the other dogs and not random
random.shuffle(training_data)

# test if its random
for sample in training_data[:10]:
    print(sample[1])

# --------------------------------------------------------------------------------
# Create the model here and add

# x and y are input parameters

X = []
y = []

# label the stuff
for features, label in training_data:
    X.append(features)
    y.append(label)

# print(X[0].reshape(-1, IMG_SIZE, IMG_SIZE, 1))

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1) #1  for grayscale single channel images, 3  for standard RGB images

# safe the stuff

pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()


