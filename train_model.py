import pickle

from tensorflow.python.keras import Sequential
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.python.keras.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense

# https://pythonprogramming.net/convolutional-neural-network-deep-learning-python-tensorflow-keras/?completed=/loading-custom-data-deep-learning-python-tensorflow-keras/
name = "fitml-CNN"

pickle_in = open("X.pickle", "rb")
X = pickle.load(pickle_in)

pickle_in = open("y.pickle", "rb")
y = pickle.load(pickle_in)

IMG_SIZE = 224
X = X / 255.0


dense_layers = [0]
layer_sizes = [128]
conv_layers = [6] #default 3

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            name = "{}-conv-{}-dense-{}".format(conv_layer, layer_size, dense_layer)
            print(name)

            model = Sequential() #init model

            model.add(Conv2D(layer_size, (3, 3), input_shape=(IMG_SIZE, IMG_SIZE, 1))) #1  for grayscale single channel images, 3  for standard RGB images
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))

            for l in range(conv_layer-1):
                model.add(Conv2D(layer_size, (3, 3)))
                model.add(Activation('relu'))
                model.add(MaxPooling2D(pool_size=(2, 2)))

            model.add(Flatten())

            for _ in range(dense_layer):
                model.add(Dense(layer_size))
                model.add(Activation('relu'))

            # model.add(Dense(1))
            model.add(Dense(1))
            model.add(Activation('sigmoid'))

            tensorboard = TensorBoard(log_dir="data/logs/{}".format(name))

            model.compile(loss='binary_crossentropy',
                          optimizer='adam',
                          metrics=['accuracy'],
                          )
            # trains the model
            # epochs are the round it will take, it can overfit for to much epochs
            model.fit(X, y,
                      batch_size=1,
                      epochs=10,
                      validation_split=0.3,
                      callbacks=[tensorboard])



model.save('data/models/fitml_grey.model')
