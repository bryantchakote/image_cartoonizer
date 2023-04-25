# TO DO: import necessary libraries (Franck)
import cv2
import matplotlib.pyplot as plt
import random
import os
import logging
import shutil

# Create and configure logger
logging.basicConfig(filename='../logs/split.log',
                    format='%(asctime)s %(lineno)d %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

# TO DO: load data fully from the directory. (Adetutu))
current_dir = os.getcwd()
data_dir_transform = os.path.join(current_dir, '../data/transformed_images')

# TO DO: split the dataset into train and test(Adetutu and Bryan)
train_size = .8
n = len(os.listdir(data_dir_transform))
indices = list(range(n))
random.shuffle(indices)
train_indices = indices[:int(train_size*n)]
test_indices = indices[int(train_size*n):]
logger.info(f'{n}, {len(train_indices)}, {len(test_indices)}')
train_dir = '../data/train'
test_dir = '../data/test'

# Train
if not os.path.exists(train_dir):
    logger.info('Creating training folder')
    try:
        os.makedirs(train_dir)
    except Exception as e:
        logger.error(e)

for index in train_indices:
    src = os.path.join(data_dir_transform, os.listdir(data_dir_transform)[index])
    dst = os.path.join(train_dir, os.listdir(data_dir_transform)[index])
    shutil.copyfile(src, dst)

# Test
if not os.path.exists(test_dir):
    logger.info('Creating testing folder')
    try:
        os.makedirs(test_dir)
    except Exception as e:
        logger.error(e)

for index in test_indices:
    src = os.path.join(data_dir_transform, os.listdir(data_dir_transform)[index])
    dst = os.path.join(test_dir, os.listdir(data_dir_transform)[index])
    shutil.copyfile(src, dst)


# TO DO: save images in a folder of train and test (Daniella)