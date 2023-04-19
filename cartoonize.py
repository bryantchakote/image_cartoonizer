# TO DO: import necessary libraries (Franck)
#import cv2
#import matplotlib.pyplot as plt
import logging
import os
from pathlib import Path

# Create and configure logger
logging.basicConfig(filename="preprocess.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

img = None #image default definition

logger.info('Accessing the folder of images')
try:
    current_dir = os.getcwd()
    data_dir = os.path.join(current_dir,'data/renamed_images')
except Exception as e:
    logger.error(e)

# TO DO: choose the method randomly to cartoonize (Adetutu and Bryan)
logger.info('Cartoonization process on the images')
try:
    #Add your code here
except Exception as e:
    logger.error(e)

# TO DO:save images in a folder (Daniella/Adetutu)
logger.info('Creating the transform image folder and storing the images transformed')
try:
    filename = ""
    data_dir = os.path.join(current_dir, 'transformed_images') # defining the transformes imafe folder
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    cv2.imwrite(filename, img)

except Exception as e:
    logger.error(e)
