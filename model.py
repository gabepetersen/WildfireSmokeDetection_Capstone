from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import cv2
import os
from grid_label import redrawBoxes, read_video
import random
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

no_smoke = os.listdir('FrameExtractor/ImageSegments/NoSmoke/')
smoke = os.listdir('FrameExtractor/ImageSegments/SmokeFrames/')
random.seed(0)


# iterates over images in a directory and appends array representation to a list.
# this function is called on a smoke directory and on the non smoke directory
# @params:
# training_data - list of data present in array between each function call
# path - path to the data to add to training_data array
# label - defined label for the smoke / nonsmoke images
# [0, 1] denotes smoke image
# [1, 0] denotes non smoke image
# files - list of files contained in the path directory
def create_training_data(training_data, path, label, files):
    for img in files:
        new_path = os.path.join(path, img)
        img = cv2.imread(new_path)
        training_data.append([np.array(img), np.array(label)])
        if len(training_data) % 10000 == 0:
            print(len(training_data))


# Use tensorflow functions to create a CNN
# The following links have documentation on the functions used to create the CNN
# http://tflearn.org/layers/conv/
# http://tflearn.org/layers/core/
# @params:
# none
# @returns:
# model - uninitialized CNN
def create_cnn():
    convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')
    convnet = conv_2d(convnet, 32, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 64, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 128, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 64, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 32, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)

    convnet = fully_connected(convnet, 2, activation='softmax')
    convnet = regression(convnet, optimizer='adam', learning_rate=LR,
                         loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')
    return model


# takes in created uninitialized CNN and trains weights using train / validation data
# @params:
# train - 120x120x3 array representing results of preprocessed videos
# test - 120x120x3 array representing some results of preprocessed videos
# model - uninitialized CNN
# MODEL_NAME - name of model defined in main
def train_cnn(train, test, model, MODEL_NAME):
    X = np.array([i[0] for i in train])  # .reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    Y = [i[1] for i in train]
    test_x = np.array([i[0] for i in test])  # .reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    test_y = [i[1] for i in test]
    model.fit({'input': X}, {'targets': Y}, n_epoch=5,
              validation_set=({'input': test_x}, {'targets': test_y}),
              snapshot_step=5, show_metric=True, run_id=MODEL_NAME)
    model.save(MODEL_NAME)


# iterate through frames of a video and call model.predict on each cell in a 16x9 grid
# if smoke is identified then draw a green box on the cell, else draw red box
# @params:
# model - trained CNN model used to predict smoke results of grids
# video - test video to run the network on
# @returns:
# nothing - displays results of grid calculation on local machine.
def grid_contour(model, video):
    done = False
    while not done:
        ret, curr_frame = video.read()
        if not ret:
            break
        else:
            frame_copy = redrawBoxes(curr_frame)
            # cv2.imshow("CurrentFrame", frame_copy)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                done = True
                break
            for x in range(0, 16):
                for y in range(0, 9):
                    xg = x * 120
                    yg = y * 120
                    grid_segment = curr_frame[yg:yg + 120, xg:xg + 120]
                    image = np.array(grid_segment).reshape(1, 120, 120, 3)
                    result = list(model.predict(image)[0])
                    max_index = result.index(max(result))
                    start = (xg, yg)
                    end = (xg + 120, yg + 120)
                    if max_index == 1:
                        color = (0, 255, 0)
                        frame_copy = cv2.rectangle(frame_copy, start, end, color, 1)
                    else:
                        color = (0, 0, 255)
                        frame_copy = cv2.rectangle(frame_copy, start, end, color, 2)
                    cv2.imshow("CurrentFrame", frame_copy)


if __name__ == '__main__':
    training_data = []
    LR = 0.00075
    IMG_SIZE = 120
    # use shuffle calls to ensure randomized data due to memory issues when creating the training_data array
    # save the data array into a file for future use
    # shuffle(smoke)
    # create_training_data(training_data, 'FrameExtractor/ImageSegments/SmokeFrames/', np.array([0, 1]), smoke[:10000])
    # shuffle(no_smoke)
    # create_training_data(training_data, 'FrameExtractor/ImageSegments/NoSmoke/', [1, 0], no_smoke[:9000])
    # shuffle(training_data)
    # np.save('train_data.npy', training_data)
    data = np.load('train_data.npy', allow_pickle=True)
    train = data[:16000]
    test = data[-3000:]
    MODEL_NAME = 'test_model_0.00075.tflearn'
    model = create_cnn()
    # call train model here if training a model with new Epoch / LR values
    # train_cnn(train, test, model, MODEL_NAME)
    # model.save(MODEL_NAME)
    # load previous saved model to eliminate need to train new model each execution of the program
    model.load(MODEL_NAME)
    path = 'Data/'
    files = os.listdir(path)
    video = read_video(path + files[3])
    grid_contour(model, video)
