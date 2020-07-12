import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # Hold the images and labels
    images = []
    labels = []

    # Go through the different sign types under gtsrb
    for signType in range(NUM_CATEGORIES):
        # The directory for the given signtype
        directory = os.path.join(data_dir, str(signType))

        for img in os.listdir(directory):
            # Get the images and resize to IMG_WIDTH x IMG_HEIGHT
            trafficSign = cv2.imread(os.path.join(directory, img))
            resizedSign = cv2.resize(trafficSign, (IMG_WIDTH, IMG_HEIGHT))

            # Add the image and label to their respective lists
            images.append(resizedSign)
            labels.append(signType)

    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # TensorFlow Model
    tfModel = tf.keras.models.Sequential([
        # Convolutional layer that learns 50 filters using a 3x3 kernel
        tf.keras.layers.Conv2D(
            50, (2, 2), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Second Convolutional layer
        tf.keras.layers.Conv2D(
            50, (2, 2), activation="relu",
        ),

        # Flatten Units
        tf.keras.layers.Flatten(),

        # Add Hidden Layers
        tf.keras.layers.Dense(50, activation="relu"),
        tf.keras.layers.Dense(50, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="relu"),
        
        # Dropout 25% of the data
        tf.keras.layers.Dropout(0.25),

        # Add Output layer for different traffic signs
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    tfModel.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return tfModel


if __name__ == "__main__":
    main()
