"""@package util
"""

import tensorflow as tf


def main():
    """
    Converts a tf graph to a TFLite model.
    """
    graph_def_file = "../data/models/retrain/retrained_graph.pb"
    input_arrays = ["input"]
    output_arrays = ["final_result"]

    converter = tf.contrib.lite.TFLiteConverter.from_frozen_graph(
        graph_def_file, input_arrays, output_arrays)
    tflite_model = converter.convert()
    open("../data/models/retrain/lite_model_retrained.tflite", "wb").write(tflite_model)


if __name__ == "__main__":
    main()
