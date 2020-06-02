# keras_model_v2_train.py
# 14 Apr 2020
# implement with recent version of keras and tensorflow
# code is referenced from: https://www.geeksforgeeks.org/python-image-classification-using-keras/

import cv2
import numpy as np
import os
from random import shuffle
import matplotlib.pyplot as plt
# keras imports
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import *
from keras.optimizers import *
from keras import backend as K 
from keras.utils import plot_model

##
##  TO RUN:
##  make sure theres directories in this directory as such:
##
##  training/
##    -- NoSmoke/
##      -- 8000 images of non smoke
##    -- Smoke/
##      -- 8000 images of smoke
##  validation/
##    -- NoSmoke/
##      -- 3000 images of non smoke
##    -- Smoke/
##      -- 3000 images of smoke
##
## (sample sizes can be adjusted in code below)

if __name__ == '__main__':
  # get training and validation set
  img_width, img_height = 120, 120
  
  train_data_dir = 'training'
  validation_data_dir = 'validation'
  nb_train_samples = 16000
  nb_validation_samples = 6000
  epochs = 50
  batch_size = 32
  
  # Since this file is mainly for experimentaion purposes, we wanted to make
  # the model easy to create and understand, so most of the code is referenced
  # from the code at the link below
  # https://www.geeksforgeeks.org/python-image-classification-using-keras/
  if K.image_data_format() == 'channels_first': 
    input_shape = (3, img_width, img_height) 
  else: 
    input_shape = (img_width, img_height, 3) 
  
  model = Sequential() 
  # first conv
  model.add(Conv2D(32, (2, 2), input_shape = input_shape)) 
  model.add(Activation('relu')) 
  model.add(MaxPooling2D(pool_size =(2, 2))) 
  
  # second conv
  model.add(Conv2D(32, (2, 2))) 
  model.add(Activation('relu')) 
  model.add(MaxPooling2D(pool_size =(2, 2))) 
  
  # third conv
  model.add(Conv2D(64, (2, 2))) 
  model.add(Activation('relu')) 
  model.add(MaxPooling2D(pool_size =(2, 2))) 
  
  model.add(Flatten()) 
  model.add(Dense(64)) 
  model.add(Activation('relu')) 
  model.add(Dropout(0.5)) 
  model.add(Dense(1)) 
  model.add(Activation('sigmoid')) 
  
  model.compile(loss ='binary_crossentropy', 
                optimizer ='rmsprop', 
                metrics =['accuracy']) 
  
  train_datagen = ImageDataGenerator( 
                    rescale = 1. / 255, 
                    shear_range = 0.2, 
                    zoom_range = 0.2, 
                    horizontal_flip = True) 
  
  test_datagen = ImageDataGenerator(rescale = 1. / 255) 
  
  # get data from training directory
  train_generator = train_datagen.flow_from_directory(train_data_dir, 
                        target_size =(img_width, img_height), 
                        batch_size = batch_size, class_mode ='binary') 
  
  # get data from validation directory
  validation_generator = test_datagen.flow_from_directory( 
                                    validation_data_dir, 
                                    target_size =(img_width, img_height), 
                                    batch_size = batch_size, class_mode ='binary') 
  
  # train up the model given the epochs
  history = model.fit_generator(train_generator, 
    steps_per_epoch = nb_train_samples // batch_size, 
    epochs = epochs, validation_data = validation_generator, 
    validation_steps = nb_validation_samples // batch_size) 
  
  # save the model
  model.save('model_saved.h5')
  
  #### if you have graphviz then you can uncomment this line
  # plot_model(model, to_file="keras_modelplot.png")

  # Plot training & validation accuracy values
  plt.plot(history.history['acc'])
  plt.plot(history.history['val_acc'])
  plt.title('Model accuracy')
  plt.ylabel('Accuracy')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Test'], loc='upper left')
  plt.show()

  # Plot training & validation loss values
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('Model loss')
  plt.ylabel('Loss')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Test'], loc='upper left')
  plt.show()