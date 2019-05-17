# FitMLModel
This project contains the retrained model and a model trained from scratch

## Getting started
- data folder contains all non python files (like logs, models, images, ...)
- util folder contains the utils to download youtube videos and convert models to TFLite

### Prerequisites
Install the following:

```
# python3 required
# install all dependencies in requirements.txt
python -r install requirements.txt
```

### Get data from youtube
Getting the videos from youtube which are found in youtube_downloader.json and extract the frame from it.
The frames will be scaled to 224x224
Script in util folder.
```
cd util
python youtube_downloader.py
```

### Manually label frames
To label the frames put it from data/frames in the right folder under data/classif.
The folder name is the label

### Prepare data
Run the following command to generate pickle file
```
cd retrain
python retrain_V2.py
```

### Retrain model
Script in retrained folder.
To retrain the existing MobileNet V2 model run following command

```
cd retrain
python retrain_V2.py
```
or 
```
python -m retrain.retrain --bottleneck_dir=data/bottlenecks
--how_many_training_steps=500
--model_dir=data/models/
--summaries_dir=data/logs/retrain/"mobilenet_1.0_224"
--output_graph=data/models/retrain/retrained_graph.pb
--output_labels=data/models/retrain/retrained_labels.txt
--architecture=mobilenet_1.0_224
--image_dir=data/classif
```

### Validate model
Script in retrained folder.
```
cd retrain
python validate_V2
```

### Convert to TFLite
Change model names in the used script!
If a graph is used than use
```
cd util
python convert_graph_to_tflite.py
```
If a Keras H5 is used than execute the following command
```
cd util
python convert_h5_to_tflite.py
```

### Tensorboard
```
tensorboard --logdir data/logs --host 127.0.0.1 &
# kill all tensorboard processes
pkill -f "tensorboard"
```
