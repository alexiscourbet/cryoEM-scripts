# cryoEM-scripts
Misceallenous scripts for cryoEM data collection and processing

#cluster_images
Script used to cluster Krios images collected with beam shift. This script computes clusters using the Kmeans algorithm based on x/y beam shift data (Beamshift_input.txt file), and clusters images accordingly.

#cryoML_CNN_analyzer
This script uses a convolutional neural network to discriminate between good and bad cryoEM images and clusters them accordingly. The CNN model (cryoML_CNN_model.model) was trained on thoushands of experimental Krios images (containing good/bad ice, CTF, particle density, etc..)

#house_keeping
Simple script to manage cryoEM images.


