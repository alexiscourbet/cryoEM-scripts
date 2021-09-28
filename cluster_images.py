#!/usr/bin/env python

#Alexis Courbet: Let me know how I can improve that and write some more stuff, always happy to help!
#acourbet@uw.edu

# Usage :
# python cluster_images.py <number of groups you want to cluster the data into> <Beam_shift_input_file>

import sys
import re
import glob, os, shutil
import numpy as np
import pandas as pd
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans2, whiten
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

number_of_clusters = int(sys.argv[1])
Beam_shift_input_file = sys.argv[2]


print "Cleaning input data..."
with open(Beam_shift_input_file,"r") as f:
    content = f.readlines()
    content = content[3:]
data = pd.DataFrame(content)
data.drop(data.tail(1).index,inplace=True)
data.columns = ["dummy_column"]
data.dropna(inplace = True)

# new data frame with split value columns 
pretty_data = data["dummy_column"].str.split("|", n = 7, expand = True) 

# making separate column names from new data frame 
pretty_data["filename"]= pretty_data[4] 
pretty_data["image_shift_x"]= pretty_data[5].astype(float)
pretty_data["image_shift_y"]= pretty_data[6].astype(float)

# Dropping other columns we don't care about
pretty_data.drop(columns =[0,1,2,3,4,5,6,7], inplace = True) 

print "Now starting clustering using kmeans2.."
#number_of_clusters = 4 #open(sys.argv[1],"r")

coords = pretty_data.as_matrix(columns=pretty_data.columns[1:])
centers,labels = kmeans2(whiten(coords), number_of_clusters, iter = 20)  

#db = DBSCAN(eps=eps, min_samples=ms, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))

print "Let's have a look at the clusters to make sure they make sense: plotting clusters.png"
plt.scatter(coords[:,0], coords[:,1], c=labels)
plt.ylim(-0.6e-05, 0.7e-05)
plt.xlim(-0.6e-05, 0.7e-05)
plt.savefig('clusters.png',dpi=100)
plt.show()

print "Let's make sure clusters are coherent: plotting cluster_histogram.png" 
cluster_map = pd.DataFrame()
cluster_map['data_index'] = pretty_data['filename'].astype(str)
cluster_map['cluster_number'] = labels
ax = cluster_map.plot.hist(bins=12, alpha=0.5)
cluster_map.head()
fig = ax.get_figure()
fig.savefig("cluster_histogram.png")

print 'Now writing', number_of_clusters, 'different files with image names corresponding to each clusters...'
for i in range (0 , number_of_clusters):
    tmps = 'cluster' + '%s' %i
    if (cluster_map["cluster_number"] == i).any():
        tmps = cluster_map[cluster_map["cluster_number"] == i]
        tmps.to_csv(r'cluster_%s.txt' %i, header=None, index=None, sep="\t", quoting=csv.QUOTE_NONE, quotechar="",  escapechar="\\")

print "Done"