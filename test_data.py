import cv2
import tensorflow as tf

CATEGORIES = ["push_up_up", "push_up_down", "squat_up", "squat_down"]


def prepare(filepath):
    IMG_SIZE = 224  # 50 in txt-based
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1) #1  for grayscale single channel images, 3  for standard RGB images


model = tf.keras.models.load_model("data/models/fitml_grey.model")

#first test
prediction = model.predict([prepare('/Users/reder/Desktop/Liegestuetze-Startposition.jpg')])
print(prediction)  # will be a list in a list.
print(CATEGORIES[int(prediction[0][0])])

#second test
prediction = model.predict([prepare('/Users/reder/Desktop/66995325001_1470505746001_vs-1470507208001.jpg')])
print(prediction)  # will be a list in a list.
print(CATEGORIES[int(prediction[0][0])])