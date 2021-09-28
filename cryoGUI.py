import Tkinter as tk
from PIL import ImageTk,Image
import sys
import re
import os, os.path
import numpy as np
import pandas as pd
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')
import sys, select

#img_dir = str(sys.argv[1])

# Create empty list for coordinate arrays to be appended to
coords = []

# Function to be called when mouse is clicked
def save_coords(event):
    click_loc = [event.x, event.y]
    print ("you clicked on", click_loc)
    coords.append(click_loc)

# Function to load the next image into the Label
def next_img():
    img_label.img = ImageTk.PhotoImage(Image.open(next(imgs)))
    img_label.config(image=img_label.img)
    
root = tk.Tk()

# Choose multiple images
img_dir =  'images2'  ##askdirectory(parent=root, initialdir=".", title='Choose folder')
#os.chdir(img_dir)
imgs = iter(os.listdir(img_dir))

img_label = tk.Label(root)
img_label.pack()
img_label.bind("<Button-1>",save_coords)

btn = tk.Button(root, text='Next image', command=next_img)
btn.pack()

next_img() # load first image

root.mainloop()

print (coords)