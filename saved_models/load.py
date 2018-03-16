import numpy as np
import keras.models
from keras.models import model_from_json
from scipy.misc import imread, imresize, imshow
import os

def init():
  this_file = os.path.abspath(__file__)
  this_dir = os.path.dirname(this_file)
  with open(os.path.join(this_dir,'resnet_model_best.json'), 'r') as json_file:
    loaded_model_json = json_file.read()
  loaded_model = model_from_json(loaded_model_json)
  loaded_model.load_weights(os.path.join(this_dir,'weights.best.resnet.hdf5'))
  print('Loaded model from disk')

  loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

  return loaded_model