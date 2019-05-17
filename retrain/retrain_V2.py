"""@package retrain
"""

import pickle

import numpy as np
from skimage.transform import resize
from sklearn.utils import shuffle
from tensorflow.python.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.python.keras.layers import Dense, Input, Dropout
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.utils import to_categorical

target_size = 224

pickle_in = open("X.pickle", "rb")
X = pickle.load(pickle_in)

pickle_in = open("y.pickle", "rb")
y = pickle.load(pickle_in)

X = X / 225.0
y = to_categorical(y, num_classes=4)


def preprocess_image(x):
    """
    Resizes the image
    :param x: image
    :return: the image array
    """
    # Resize the image to have the shape of (224, 224)
    x = resize(x, (target_size, target_size),
               mode='constant',
               anti_aliasing=False)

    # convert to 3 channel (RGB)
    x = np.stack((x,) * 3, axis=2)

    # Make sure it is a float32, here is why
    # https://www.quora.com/When-should-I-use-tf-float32-vs-tf-float64-in-TensorFlow
    return x.astype(np.float32)


def load_data_generator(x, y, batch_size=64):
    """
    Creates a generator with images for training the model.

    :param x: image data
    :param y: label data
    :param batch_size: size of one batch
    :return:
    """
    num_samples = x.shape[0]
    while 1:  # Loop forever so the generator never terminates
        try:
            shuffle(x)
            for i in range(0, num_samples, batch_size):
                x_data = [preprocess_image(im) for im in x[i:i + batch_size]]
                y_data = y[i:i + batch_size]

                # convert to numpy array since this what keras required
                yield shuffle(np.array(x_data), np.array(y_data))
        except Exception as err:
            print(err)


def build_model():
    """
    Loads the MobileNetV2 model for keras. Adds new dense and dropout layers to the output.
    :return: the model
    """
    input_tensor = Input(shape=(target_size, target_size, 3))
    base_model = MobileNetV2(
        include_top=False,
        weights='imagenet',
        input_tensor=input_tensor,
        input_shape=(target_size, target_size, 3),
        pooling='avg')

    for layer in base_model.layers:
        layer.trainable = False

    op = Dense(256, activation='relu')(base_model.output)
    op = Dropout(.25)(op)

    ##
    # softmax: calculates a probability for every possible class.
    #
    # activation='softmax': return the highest probability;
    # for example, if 'Coat' is the highest probability then the result would be
    # something like [0,0,0,0,1,0,0,0,0,0] with 1 in index 5 indicate 'Coat' in our case.
    ##
    output_tensor = Dense(4, activation='softmax')(op)

    model = Model(inputs=input_tensor, outputs=output_tensor)

    return model


def main():
    tensorboard = TensorBoard(log_dir="../data/logs/retrain/v2")

    model = build_model()
    model.compile(optimizer=Adam(),
                  loss='categorical_crossentropy',
                  metrics=['categorical_accuracy'])

    train_generator = load_data_generator(X, y, batch_size=64)
    model.fit_generator(train_generator,
                        steps_per_epoch=100,
                        verbose=1,
                        epochs=2,
                        callbacks=[tensorboard])

    # save the model
    model_name = "tf_serving_keras_mobilenetv2"
    model.save(f"../data/models/{model_name}.h5")


if __name__ == "__main__":
    main()
