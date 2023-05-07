from time import time
import logging
import os
import sys
import shutil
from natsort import natsorted
import cv2
import random
import cartoonization_methods
from utils import create_if_not_exist_or_delete_everything_inside
from tqdm import tqdm

# Start
start = time()

# Current directory
current_dir = os.getcwd()

# Create and configure the logger
log_file_path = os.path.join(current_dir, '../logs/cartoonization.log')
logging.basicConfig(
    filename=log_file_path,
    filemode='w',
    format='%(asctime)s - %(filename)s line %(lineno)d - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger()

# Access the groundtruth images directory
msg = 'Accessing the images directory...'
print(msg), logger.info(msg)

groundtruth_images_dir = os.path.join(current_dir, '../data/groundtruth_images')

if os.path.exists(groundtruth_images_dir):
    msg = 'Successfully accessed ' + groundtruth_images_dir
    print(msg), logger.info(msg)
else:
    msg = groundtruth_images_dir + ' not found'
    print(msg), logger.error(msg)
    sys.exit()

# Cartoonize the images
msg = 'Start cartoonizing...'
print(msg), logger.info(msg)
msg = 'Creating the cartoonized images directory...'
print(msg), logger.info(msg)

## Preparing the cartoonized images directory
cartoonized_images_dir = os.path.join(current_dir, '../data/cartoonized_images')
create_if_not_exist_or_delete_everything_inside(cartoonized_images_dir)

## Cartoonification process
msg = 'Cartoonization running...'
print(msg), logger.info(msg)
for image_file in tqdm(natsorted(os.listdir(groundtruth_images_dir))):
    ### Read the image
    image_path = os.path.join(groundtruth_images_dir, image_file)
    try:
        image = cv2.imread(image_path)
    except Exception as e:
        print(e), logger.error(e)
    else:
        if image is not None:
            logger.info(f'{image_path}, loaded successfully')
            ### Choose a method and use it
            try:
                #### Select only the functions from the cartoonization_methods module
                functions = [func for func in dir(cartoonization_methods) if callable(getattr(cartoonization_methods, func))]
                    
                #### Pick one of them
                cartoonizer = random.choice(functions)

                #### Call it on the image
                cartoon = getattr(cartoonization_methods, cartoonizer)(image)
            except Exception as e:
                print(e), logger.error(e)
            else:
                try:
                    ### Convert the BGR image to RGB
                    # cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
                    pass
                except Exception as e:
                    print(e), logger.error(e)
                else:
                    ### Save the cartoonized image
                    cartoonized_image_path = os.path.join(cartoonized_images_dir, image_file)
                    try:
                        cv2.imwrite(cartoonized_image_path, cartoon)
                        logger.info(f'Cartoonized image saved to {cartoonized_image_path}')
                    except Exception as e:
                        print(e), logger.error(e)
        else:
            msg = f'{image_path} couldn\'t be read'
            print(msg), logger.error(msg)
msg = 'Done'
print(msg), logger.info(msg)

# End
end = time() - start
msg = f'Cartoonization finished within {end}s'
print(msg), logger.info(msg)
