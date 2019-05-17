"""@package retrain
"""

import os.path

import cv2
import numpy as np
from skimage.transform import resize
from tensorflow.python.keras.models import load_model

CATEGORIES = ["push_up_down", "push_up_up", "squat_down", "squat_up"]
VALIDATION_IMAGE_PATH = "../data/validate"
MODEL_NAME = "tf_serving_keras_mobilenetv2.h5"
MODEL_PATH = "../data/models/"
IMG_SIZE = 224


def prepare(filepath):
    """
    reads an image in grayscale and rezises it to IMG_SIZE * IMG_SIZE

    :param filepath: to the image
    :return: numpay array of the grayscale image
    """
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = resize(img_array, (IMG_SIZE, IMG_SIZE))
    new_array = np.stack((new_array,) * 3, axis=2)
    new_array = np.expand_dims(new_array, 0)
    print(new_array.shape)
    return new_array


def main():
    """
    loads the retrained module and executes a prediction on the test images

    there is a problem with load_model in keras when a retrained mobile net model is saved.
    See: https://github.com/tensorflow/tensorflow/issues/22697

    """
    model_full_path = os.path.join(MODEL_PATH, MODEL_NAME)

    #
    model = load_model(model_full_path)

    image = prepare(os.path.join(VALIDATION_IMAGE_PATH, "push_up_up", "01.jpg"))
    prediction = model.predict(image)
    print(prediction)
    index = np.argmax(prediction[0])
    print(f"Predicted label is: {CATEGORIES[index]}")


if __name__ == "__main__":
    main()
