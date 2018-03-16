from scipy.misc import imsave, imread, imresize
import numpy as np
import keras.models
from keras.preprocessing import image  
from keras.applications.resnet50 import preprocess_input, decode_predictions
from tqdm import tqdm 
from keras.applications.resnet50 import ResNet50
import cv2

class PredictionEngine:
  def __init__(self, model, dog_names):
    self.model = model
    self.face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')
    self.dog_names = dog_names
    self.ResNet50_model = ResNet50(weights='imagenet')

  def extract_Resnet50(self, tensor):
    from keras.applications.resnet50 import ResNet50, preprocess_input
    return ResNet50(weights='imagenet', include_top=False).predict(preprocess_input(tensor))

  # returns "True" if face is detected in image stored at img_path
  def face_detector(self, img_path):
      img = cv2.imread(img_path)
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      faces = self.face_cascade.detectMultiScale(gray)
      return len(faces) > 0

  def path_to_tensor(self, img_path):
      # loads RGB image as PIL.Image.Image type
      img = image.load_img(img_path, target_size=(224, 224))
      # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
      x = image.img_to_array(img)
      # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
      return np.expand_dims(x, axis=0)

  def paths_to_tensor(self, img_paths):
      list_of_tensors = [self.path_to_tensor(img_path) for img_path in tqdm(img_paths)]
      return np.vstack(list_of_tensors)


  # ### Making Predictions with ResNet-50
  def ResNet50_predict_labels(self, img_path):
      # returns prediction vector for image located at img_path
      img = preprocess_input(self.path_to_tensor(img_path))
      return np.argmax(self.ResNet50_model.predict(img))


  # ### Write a Dog Detector
  ### returns "True" if a dog is detected in the image stored at img_path
  def dog_detector(self, img_path):
      prediction = self.ResNet50_predict_labels(img_path)
      return ((prediction <= 268) & (prediction >= 151)) 

  def convertImage(self, imgData):
    imgstr = re.search(r'base64,(.*)',imgData1).group(1)
    with open('output.png','wb') as output:
      output.write(imgstr.decode('base64'))


  def resnet_predict_breed(self, img_path):
      # extract bottleneck features
      bottleneck_feature = self.extract_Resnet50(self.path_to_tensor(img_path))
      # obtain predicted vector
      predicted_vector = self.model.predict(bottleneck_feature)
      # return dog breed that is predicted by the model    
      return self.dog_names[np.argmax(predicted_vector)]


  def predict_breed(self, img_path):
      if self.face_detector(img_path):
          breed = self.resnet_predict_breed(img_path)
          
          return {'res': breed,
                 'code': 0}
      elif self.dog_detector(img_path):
          breed = self.resnet_predict_breed(img_path)
          
          return {'res': breed,
                 'code': 1}
      else:
          return {'res': 'Neither a dog nor a human was detected',
                 'code': 2}

