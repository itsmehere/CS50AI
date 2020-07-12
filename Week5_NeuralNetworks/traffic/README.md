# Traffic

Write an AI to identify which traffic sign appears in a photograph.

## Background:

As research continues in the development of self-driving cars, one of the key challenges is [computer vision](https://en.wikipedia.org/wiki/Computer_vision), allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.

In this project, you’ll use [TensorFlow](https://www.tensorflow.org/) to build a neural network to classify road signs based on an image of those signs. To do so, you’ll need a labeled dataset: a collection of images that have already been categorized by the road sign represented in them.

Several such data sets exist, but for this project, we’ll use the [German Traffic Sign Recognition Benchmark](http://benchmark.ini.rub.de/?section=gtsrb&subsection=news) (GTSRB) dataset, which contains thousands of images of 43 different kinds of road signs.

## Installation:

Inside the `traffic` directory, run `pip3 install -r requirements.txt` to install this project's dependencies:  
- `opencv-python`: Image Processing
- `scikit-learn`: Machine Learning related functions
- `tensorflow`: Neural Networks

## Understanding:

First, take a look at the data set by opening the `gtsrb` directory. You’ll notice 43 subdirectories in this dataset, numbered `0` through `42`. Each numbered subdirectory represents a different category (a different type of road sign). Within each traffic sign’s directory is a collection of images of that type of traffic sign.

Next, take a look at `traffic.py`. In the `main` function, we accept as command-line arguments a directory containing the data and (optionally) a filename to which to save the trained model. The data and corresponding labels are then loaded from the data directory (via the `load_data` function) and split into training and testing sets. After that, the `get_model` function is called to obtain a compiled neural network that is then fitted on the training data. The model is then evaluated on the testing data. Finally, if a model filename was provided, the trained model is saved to disk.

## My Output:

```
C:\Users\mihir\Programming\CS50AI\Week5_NeuralNetworks\traffic>python traffic.py gtsrb
Loading Data from GTSRB...
Epoch 1/10
500/500 [==============================] - 10s 19ms/step - loss: 1.9013 - accuracy: 0.4972
Epoch 2/10
500/500 [==============================] - 9s 19ms/step - loss: 0.6460 - accuracy: 0.8106
Epoch 3/10
500/500 [==============================] - 9s 19ms/step - loss: 0.3805 - accuracy: 0.8939
Epoch 4/10
500/500 [==============================] - 9s 19ms/step - loss: 0.2854 - accuracy: 0.9224
Epoch 5/10
500/500 [==============================] - 10s 21ms/step - loss: 0.2122 - accuracy: 0.9414
Epoch 6/10
500/500 [==============================] - 9s 18ms/step - loss: 0.2075 - accuracy: 0.9437
Epoch 7/10
500/500 [==============================] - 9s 18ms/step - loss: 0.1652 - accuracy: 0.9553
Epoch 8/10
500/500 [==============================] - 9s 19ms/step - loss: 0.1740 - accuracy: 0.9532
Epoch 9/10
500/500 [==============================] - 9s 19ms/step - loss: 0.1257 - accuracy: 0.9668
Epoch 10/10
500/500 [==============================] - 9s 19ms/step - loss: 0.1095 - accuracy: 0.9722
333/333 - 2s - loss: 0.1388 - accuracy: 0.9659
```

## Other Links:

Read more about cs50ai [here](https://cs50.harvard.edu/ai/2020/)   
[Original Problem Page](https://cs50.harvard.edu/ai/2020/projects/5/traffic/)