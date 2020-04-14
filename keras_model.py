from grid_label import redrawBoxes, read_video
from model import grid_contour
import numpy as np
import cv2
import os
import random
import keras
from keras.models import Sequential
import keras, os
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np


# Function to create validation data. This function selects a subset of data
# (~20% using my set of 300 videos) which is defined by the user (see the length parameter in the for loop)
# to be taken and used as validation data during training. 
# To ensure the randomized nature of the data, use the function random.shuffle. 
# User must specify their own file path to their smoke / nosmoke data in main and pass as a parameter to the function
# @params path_src: string - path to the whole set of training data for either smoke or not smoke data
# @params path_dest: string - path to the directory which houses a subset of training data for the specified path_src
def create_validation_data(path_src, path_dest):
    # move 20% smoke files to validation set
    #random.shuffle()
    print(path_src)
    print(path_dest)
    files = os.listdir(path_src)
    src = [path_src + '/' + files[i] for i in range(len(files))]
    dest = [path_dest + '/' + files[i] for i in range(len(files))]
    for i in range(40000):
        os.rename(src[i], dest[i])

# Function to create a sequential model CNN 
# CNN takes input shape of 120x120x3 which is the size of our images in the training data 
# Afterwards, the following is added to the model - taken from https://towardsdatascience.com/step-by-step-vgg16-implementation-in-keras-for-beginners-a833c686ae6c
# 2 x convolution layer of 64 channel of 3x3 kernal and same padding
# 1 x maxpool layer of 2x2 pool size and stride 2x2
# 2 x convolution layer of 128 channel of 3x3 kernal and same padding
# 1 x maxpool layer of 2x2 pool size and stride 2x2
# 3 x convolution layer of 256 channel of 3x3 kernal and same padding
# 1 x maxpool layer of 2x2 pool size and stride 2x2
# 3 x convolution layer of 512 channel of 3x3 kernal and same padding
# 1 x maxpool layer of 2x2 pool size and stride 2x2
# 3 x convolution layer of 512 channel of 3x3 kernal and same padding
# 1 x maxpool layer of 2x2 pool size and stride 2x2
# relu activation used to prevent the propagation of negative values
# Dense layers flatten the the vector containing the convolutions in order to obtain a prediction

def create_cnn():
    model = Sequential()
    model.add(Conv2D(input_shape=(120, 120, 3), filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(filters=256, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=256, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=256, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(Conv2D(filters=512, kernel_size=(3, 3), padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Flatten())
    model.add(Dense(units=4096, activation="relu"))
    model.add(Dense(units=4096, activation="relu"))
    model.add(Dense(units=2, activation="softmax"))
    return model

# Function to compile CNN.
# learning rate of 0.001 defined for compilation - decrease in the event of significant bouncing 
# of outcomes between epochs in order to obtain a global minimum.
# @params: model - a created cnn model
def compile_cnn(model):
    opt = Adam(lr=0.001)
    model.compile(optimizer=opt, loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])


# Function to run the model on testing and validation data
# monitor valdiatoin accuracy via val_acc passed to the monitor argument in ModelCheckpoint. 
# CNN is updated only in the event the current epoch is greater than the last epoch value for val_acc
# Early stopping halts execution of model in the event no improvement is found in the assigned number of epochs. 
# Default is set to 10.
# User can alter number of epochs from 100 to any number in the fit_generator method. 
# @params: model - a compiled cnn model 
def run_cnn(model):
    checkpoint = ModelCheckpoint("vgg16_1.h5", monitor='val_acc', verbose=1, save_best_only=True,
                                 save_weights_only=False, mode='auto', period=1)
    early = EarlyStopping(monitor='val_acc', min_delta=0, patience=10, verbose=1, mode='auto')
    hist = model.fit_generator(steps_per_epoch=100, generator=traindata, validation_data=testdata, validation_steps=10,
                               epochs=100, callbacks=[checkpoint, early])

if __name__ == '__main__':
#    make the same create_validation_data call for smoke data.

#    path_src = os.getcwd() + '/FrameExtractor/ImageSegments/Train/NoSmoke'
#    path_dest = os.getcwd() + '/FrameExtractor/ImageSegments/Train/NoSmokeTest'
#    create_validation_data(path_src, path_dest)

    path_train = os.getcwd() + '/FrameExtractor/ImageSegments/Train/'
    path_test = os.getcwd() + '/FrameExtractor/ImageSegments/Test/'
    

    # create ImageDataGenerator object to label all images contained in path_train directory
    trdata = ImageDataGenerator()
    traindata = trdata.flow_from_directory(directory=path_train, target_size=(120, 120))

    # create ImageDataGenerator object to label all images contained in path_test directory
    tsdata = ImageDataGenerator()
    testdata = tsdata.flow_from_directory(directory=path_test, target_size=(120, 120))

    MODEL_NAME = 'KERAS_VGG16_MODEL'
    model = create_cnn()
    compile_cnn(model)
    run_cnn(model)

    model.save(MODEL_NAME)

