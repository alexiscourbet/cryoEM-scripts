#!/usr/bin/python

#On the digs run "source activate tensorflow"
#You might have to install keras using : pip install keras

#usage:
#python cryoML_CNN_analyzer.py -i test_dir   

#Your full path to images to be tested should be in the form: test_dir1/test_dir2/*images
#In that case "test_dir1" would be what you give as an argument. You can have as many different test_dir2 as you want in the test_dir1 folder for convenience.

#Let me know how I can improve that and write some more stuff, always happy to help!
#acourbet@uw.edu

from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from sklearn.metrics import classification_report
import numpy as np
import argparse
import os, os.path
import pandas as pd
import matplotlib.pyplot as plt
import shutil

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-m", "--model", required=False, default="/home/acourbet/for/Jesse/cryoML/cryoML_CNN_model.model",
	help="path to pre-trained model, by default the directory to the model I trained")
args = vars(ap.parse_args())

# load the pre-trained network
print("Loading pre-trained cryoTinder network...")
model = load_model(args["model"])  #args["model"]

#Generating images to be input to the CNN..
test_datagen = ImageDataGenerator(rescale=1./255)
images_test_dir = args["images"]
test_generator = test_datagen.flow_from_directory(images_test_dir,  
                                                  target_size=(150, 150),
                                                  color_mode="grayscale",
                                                  batch_size=1,
                                                  class_mode=None,
                                                  shuffle=False,
                                                  seed=42)

STEP_SIZE_TEST=test_generator.n//test_generator.batch_size

#Generating predictions
test_generator.reset()
print("Processing images through the network to find matches...")
pred=model.predict_generator(test_generator,steps=STEP_SIZE_TEST,verbose=1)
print('Done! Continuing...')

#Generating classes instead of raw probabilities
cl = np.round(pred)
filenames=test_generator.filenames

#Storing results in a dataframe:
results=pd.DataFrame({"Image":filenames,"Prediction":pred[:,0], "class":cl[:,0]})
results['class'] = results['class'].map({1.0:'g00d', 0.0:'bad'}) 
g00d_results = results[results['class'].str.contains("g00d")]

print( "Saving swiping classification results to " + "results_from_" + str( args["images"] ) + ".csv ...")
results.to_csv( str( "results_from_" + str(args["images"] ) + ".csv"), index=False)

predicted_class_indices=np.argmax(pred,axis=1)
print("Printing the cryoTinder classification report..." + '\n' + '\n' + classification_report(test_generator.classes, predicted_class_indices, target_names=test_generator.class_indices.keys()))

print("Plotting prediction matches counts by class, class_counts.png...")
results['class'].value_counts().plot(kind='bar');
plt.title("Prediction matches counts by class")
plt.ylabel("Counts")
plt.savefig("matches_counts_from_" + str(args["images"] ) + ".png")

print('Finally copying good match images to image_matches/ folder...')
good_imgs_dir = 'image_matches'

#Create target Directory if don't exist
if not os.path.exists(good_imgs_dir):
    os.mkdir(good_imgs_dir)
    print( "The " + good_imgs_dir + " directory to store your good image natches was just created!")
else:    
    print( "The " +  good_imgs_dir + "/ directory already exists!")


for i in g00d_results['Image']:
    try:
        source = args["images"] + "/" + i  #  #arggs images to test
        dest = good_imgs_dir + '/' + str(i)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(source, dest)
    except OSError as e:
        print('Image not copied. Error: %s' % e)

print('All done!')