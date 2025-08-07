from imageai.Classification.Custom import ClassificationModelTrainer
from pathlib import Path
import os

execution_path = os.getcwd()

root = Path('.')

# initiate
print('Initiating model training.')
model_trainer =  ClassificationModelTrainer()

# set model type
model_trainer.setModelTypeAsResNet50()

# dataset path
model_trainer.setDataDirectory("dataset")

# desired training metrics
number_of_objects = 8       # number of classes in our dataset
number_of_experiments = 2   # number of times the model should go over our data, epochs
batch_size = 20             # number of images the model should look at at a time when training, higher number will descrease training time, lower number will decrease training time
show_network_summary = True # print training data on terminal

# train our stated model based on the metrics stated ... removed - num_objects=number_of_objects, enhance_data=True, 
model_trainer.trainModel(num_experiments=number_of_experiments, batch_size=batch_size)

print('Training process done.')