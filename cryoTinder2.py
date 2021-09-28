#### pip install pillow
#### pip install tkinter

import Tkinter as tk
from PIL import ImageTk,Image
import sys
import re
import os, os.path
import numpy as np
import pandas as pd
import csv
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')
import sys, select
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import shutil

img_dir = str(sys.argv[1])
good_imgs_dir = 'matches'

#Create target Directory if don't exist
if not os.path.exists(good_imgs_dir):
    os.mkdir(good_imgs_dir)
    print( good_imgs_dir + " directory " + "created!")
else:    
    print( "The " +  good_imgs_dir + " directory " + "already exists!")

# Function to load the next image into the Label
def next_img():
    print ("You are checking out image: " + str(list(imgs)[-1]))
    try:
        img_label.img = ImageTk.PhotoImage(Image.open(next(imgs)))
        img_label.config(image=img_label.img)
    except StopIteration:
        return  # if there are no more images, do nothing

def next_and_save_img():
    #iteratr is an interator
    #dd = deque(iteratr, maxlen=1)
    #last_element = dd.pop()
    #last_element = str(max(enumerate(iteratr))[1])
    #last_element = reduce(lambda x,y:y,iteratr)
    #try:
       # shutil.copytree(str(list(image)[-1]), dest)
        #print('Copied this image match in you matches folder')
    # Any error saying that the directory doesn't exist
    #except OSError as e:
      #  print('Image not copied. Error: %s' % e)
    print ("You are checking out image: " + str(list(imgs)[-1]))
    try:
        img_label.img = ImageTk.PhotoImage(Image.open(next(imgs)))
        img_label.config(image=img_label.img)
    except StopIteration:
        return  # if there are no more images, do nothing




for image_file in os.scandir(img_dir):
    if (entry.path.endswith(".png")
            or entry.path.endswith(".jpeg")) and entry.is_file():
