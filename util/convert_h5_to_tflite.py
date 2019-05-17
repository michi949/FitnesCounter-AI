"""@package util
"""

import tensorflow as tf


def main():
    """
    Converts a h5 keras model to a TFLite model.
    """
    h5_file = "../data/models/tf_serving_keras_mobilenetv2.h5"

    converter = tf.contrib.lite.TFLiteConverter.from_keras_model_file(h5_file)
    tflite_model = converter.convert()
    open("../data/models/lite_retrained_keras.tflite", "wb").write(tflite_model)


if __name__ == "__main__":
    main()
