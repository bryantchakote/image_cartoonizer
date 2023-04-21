# TO DO: import necessary libraries (Franck)
import cv2
#import matplotlib.pyplot as plt
import logging
import os
from random import  *
import numpy as np
from pathlib import Path

# Create and configure logger
logging.basicConfig(filename="preprocess.log",
                    format='%(asctime)s %(lineno)d %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

img = None #image default definition
change_gray = False #tracking whether the image has been transformed to gray scale or not
filename = ''
thresh = None
cartoon = None
logger.info('Accessing the folder of images')
try:
    current_dir = os.getcwd()
    data_dir = os.path.join(current_dir,'data/renamed_images')
    logger.info(data_dir)
except Exception as e:
    logger.error(e)

# TO DO: choose the method randomly to cartoonize (Adetutu and Bryan)
logger.info('Cartoonization process on the images')
for image_file in os.listdir(data_dir):
    logger.info(os.path.join(data_dir,image_file))
    # reading image file
    image_path = os.path.join(data_dir,image_file)
    print(f'processing {image_path}')
    image = cv2.imread(image_path)
    if image is not None:

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #step1: apply filters to the image
        dst = randint(0,100)
        sigmaColor = randint(0,100)
        sigmaSpace = randint(0,100)
        grayscale = randint(0, 1)

        if grayscale == 0:
            logger.info('Filtering using original image')
            try:
                gray_smooth = cv2.bilateralFilter(image, dst, sigmaColor, sigmaSpace)
            except Exception as e:
                logger.error(e)
        else:
            logger.info('Filtering using gray scale image')
            try:
                gray_smooth = cv2.bilateralFilter(gray, dst, sigmaColor, sigmaSpace)
            except Exception as e:
                logger.error(e)
            change_gray = True

        # step2: edge extraction
        logger.info('Edge extraction')
        edge = randint(0,1)
        threshold1 = randint(0,100)
        threshold2 = randint(0,100)
        if edge == 0:
            logger.info('Canny edge extraction')
            try:
                edges = cv2.Canny(gray_smooth, threshold1, threshold2)
            except Exception as e:
                logger.error(e)
        else:
            logger.info('Adaptative threshold edge extraction')
            edge = randint(0, 1)
            block_size = randint(0, 100)
            c = randint(0, 100)
            edge_method = randint(0, 1)
            if edge_method == 0:
                logger.info('Adaptative threshold edge extraction with mean thresholding')
                try:
                    edges = cv2.adaptiveThreshold(gray_smooth, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c)
                except Exception as e:
                    logger.error(e)
            else:
                logger.info('Adaptative threshold edge extraction with gaussian thresholding')
                try:
                    edges = cv2.adaptiveThreshold(gray_smooth, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c)
                except Exception as e:
                    logger.error(e)

        # dilating some images if launched
        dilate = randint(0,1)
        if dilate == 1:
            logger.info('dilation lauched')
            kernel1 = randint(1,10)
            kernel2 = randint(1, 10)
            iter = randint(1, 10)
            kernel = np.ones((kernel1, kernel2), np.uint8)
            try:
                edges = cv2.dilate(edges, kernel, iterations=iter)
            except Exception as e:
                logger.error(e)

        # step3:Application of bitwise merging
        merge = randint(0,2)
        if merge == 0:
            logger.info('lauching the cartoonization operation with inverse bitwise')
            try:
                edges_inv = cv2.bitwise_not(edges)
                cartoon = cv2.bitwise_and(gray_smooth,gray_smooth, mask=edges_inv)
            except Exception as e:
                logger.error(e)
        elif merge == 1 and change_gray:
            logger.info('lauching the cartoonization operation with gradient')
            try:
                thresh = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                cartoon = cv2.bitwise_and(gray_smooth, thresh)
            except Exception as e:
                logger.error(e)
        else:
            logger.info('lauching the cartoonization operation with with only grayscale')
            try:
                cartoon = cv2.bitwise_and(gray_smooth, gray_smooth)
            except Exception as e:
                logger.error(e)

        logger.info('Creating the transform image folder and storing the images transformed')
        data_dir_transform = os.path.join(current_dir, 'data/transformed_images') # defining the transformes imafe folder
        logger.info('Converting cartoon back to rgb')
        try:
            cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
        except Exception as e:
            logger.error(e)
        if not os.path.exists(data_dir_transform):
            logger.info('Creating file if not exist')
            try:
                os.makedirs(data_dir_transform)
            except Exception as e:
                logger.error(e)
            logger.info('Saving image in transform folder')
            try:
                filename = os.path.join(data_dir_transform,image_file)
                print(f'saving file in {filename}')
            except Exception as e:
                logger.error(e)
            try:
                cv2.imwrite(filename, cartoon)
            except Exception as e:
                logger.error(e)

        else:
            logger.info('Saving image in transform folder')
            try:
                filename = os.path.join(data_dir_transform,image_file)
                print(f'saving file in {filename}')
            except Exception as e:
                logger.error(e)
            try:
                cv2.imwrite(filename, cartoon)
            except Exception as e:
                logger.error(e)

    else:
        print(f'found empty image {image_path}')

