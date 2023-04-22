# TO DO: Import necessary libraries (Franck)
import cv2
import logging
import os
import random
from cartoonization_methods import method_1, method_2

# Create and configure logger
logging.basicConfig(filename='../logs/cartoonization.log',
                    format='%(asctime)s %(lineno)d %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

logger.info('Accessing the folder of images')

try:
    current_dir = os.getcwd()
    data_dir = os.path.join(current_dir, '../data/renamed_images')
    logger.info(data_dir)
except Exception as e:
    logger.error(e)

# TO DO: Choose the method randomly to cartoonize (Bryan)
logger.info('Cartoonization process on the images')
logger.info('Creating the folder intended to contain transformed images')
data_dir_transform = os.path.join(current_dir, '../data/transformed_images')

if not os.path.exists(data_dir_transform):
    logger.info('Creating transformed images folder')
    try:
        os.makedirs(data_dir_transform)
    except Exception as e:
        logger.error(e)

for image_file in os.listdir(data_dir):    
    # Reading the image
    image_path = os.path.join(data_dir, image_file)
    image = cv2.imread(image_path)

    if image is not None:
        logger.info(f'{os.path.join(data_dir, image_file)}, loaded successfully')
        try:
            cartoon = random.choice([method_1, method_2])(image)
        except Exception as e:
            logger.error(e)
            continue
        else:
            try:
                # Converting images from BGR to RGB
                cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
            except Exception as e:
                logger.error(e)
            else:
                # Save the cartoonized image in the folder containing transformed images
                logger.info(f'Saving the cartoonized image to {os.path.join(data_dir_transform, image_file)}')
                try:
                    filename = os.path.join(data_dir_transform, image_file)
                    cv2.imwrite(filename, cartoon)
                except Exception as e:
                    logger.error(e)
    else:
        logger.warning(f'Image {image_path} couldn\'t be read')