from imageai.Classification.Custom import CustomImageClassification
from pathlib import Path
import os

execution_path = os.getcwd()

root = Path('.')

# state model path. Should match one of the model filenames in ->dataset->models. Usually the model that achieved the highest accuracy during training
model_path = "dataset/models/resnet50-dataset-test_acc_0.66959_epoch-1.pt"

# state json path. Should match the json file name in ->dataset->json
json_path = "dataset/models/dataset_model_classes.json"

# state number of classes in our dataset, should match the one used in training
number_of_objects = 8

# initiate prediction module
prediction = CustomImageClassification()

# set model type, should match the one used in training
prediction.setModelTypeAsResNet50()

# set model path, according to stated path
prediction.setModelPath(model_path)

# set json path, according to stated path
prediction.setJsonPath(json_path)

def classify(image_path):       # path of the image saved on image analysis request by user

    # load saved model ... removed -> num_objects=number_of_objects
    prediction.loadModel()

    # state result count, number of the top results to show. Set to class count number to show match probabilities for all classes present in our data
    result_count = number_of_objects
    
    # get predictions for each object class. A match probability is return for each object class in our data
    predictions, probabilities = prediction.classifyImage(image_path, result_count=result_count)

    # loop through predictions and their probability data
    for eachPrediction, eachProbability in zip(predictions, probabilities):

        # print results to terminal
        print(eachPrediction , " : " , eachProbability)

    # return prediction data to user request function, the one that called the classify function
    return predictions, probabilities
