#!/usr/bin/env python

# Just execute this script in your folder with your images, and it will cycle through them all and copy the ones you like in a "matches" folder. You can cycle as many times as you want if you've missed some.
# You might have to install tkinter and PIL with:
#### pip install pillow
#### pip install tkinter

#Let me know how I can improve that and write some more stuff, always happy to help!
#acourbet@uw.edu

import Tkinter as tk
from PIL import ImageTk,Image
import sys
import re
import os, os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, select
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import shutil
import itertools 

#img_dir = str(sys.argv[1])
good_imgs_dir = 'matches'

#Create target Directory if don't exist
if not os.path.exists(good_imgs_dir):
    os.mkdir(good_imgs_dir)
    print( good_imgs_dir + " directory to store your image matches created!")
else:    
    print( "The " +  good_imgs_dir + " directory already exists!")

def get_cycle_props(cycle) :
    # Get the current state
    partial = []
    n = 0
    g = next(cycle)
    while ( g not in partial ) :
        partial.append(g)
        g = next(cycle)
        n += 1
    # Cycle until the "current" (now previous) state
    for i in range(n-1) :
        g = next(cycle)
    return (partial, n, partial[0],partial[-1])

def get_cycle_list(cycle) :
    return get_cycle_props(cycle)[0]

def get_cycle_state(cycle) :
    return get_cycle_props(cycle)[2]

def get_cycle_state2(cycle) :
    return get_cycle_props(cycle)[3]

def get_cycle_len(cycle) :
    return get_cycle_props(cycle)[1]

# Function to load the next image into the Label
def next_img():
    try:
        img_label.img = ImageTk.PhotoImage(Image.open(next(imgs))) #
        img_label.config(image=img_label.img)
    except StopIteration:
        print("You've checked out all the photos arround!")
        return  # if there are no more images, do nothing

def save_img():
    try:
        source = str(get_cycle_state2(imgs))
        dest = good_imgs_dir + "/" + "match_" + str(get_cycle_state2(imgs))
        shutil.copyfile(source, dest)
        print('Copied this image match ( ' + str(get_cycle_state2(imgs)) + ' ) in your matches folder!')
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Image not copied. Error: %s' % e)
    
def print_image_name():
    print("You are now checking out image profile " + get_cycle_state(imgs) + ",  like it...?      <3  /  X ")
    
def no_match():
    print( get_cycle_state2(imgs) + " doesn't seem to be a good match for you...")

root = tk.Tk()

imgs = itertools.cycle(filter(lambda x: x.endswith(('.png','.jpeg','.jpg')), os.listdir(os.curdir)))
img_label = tk.Label(root)
img_label.pack()

command_save_and_next = lambda:[ save_img(), print_image_name(), next_img() ] 
command_pass_and_next = lambda:[ no_match(), print_image_name(), next_img() ]

btn1 = tk.Button(root, text='<3       SWIPE RIGHT      <3 ', command = command_save_and_next )
btn2 = tk.Button(root, text=' X        SWIPE LEFT        X  ', command = command_pass_and_next )
btn1.pack()
btn2.pack()

next(imgs) # load first image
img_label.img = ImageTk.PhotoImage(Image.open(get_cycle_state(imgs)))
img_label.config(image=img_label.img)
numer_of_images_to_check = str(get_cycle_len(imgs))
print('You are about to check out the first image profile out of ' + str(get_cycle_len(imgs)) + " profiles. Swipe left to start!" ) #+ "")

root.mainloop()
