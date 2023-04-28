from time import time
import os
import sys
import shutil
from utils import create_if_not_exist_or_delete_everything_inside
import logging
from tqdm import tqdm

# Start
start = time()

# Current directory
current_dir = os.getcwd()

# Create and configure the logger
log_file_path = os.path.join(current_dir, '../logs/split_by_cartoonization.log')
logging.basicConfig(
    filename=log_file_path,
    filemode='w',
    format='%(asctime)s - %(filename)s line %(lineno)d - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger()

# Read the cartoonization log file to match each image to the method used
methods_used = []

cartoonization_log_path = '../logs/cartoonize.log'
cartoonization_log_path = os.path.join(current_dir, cartoonization_log_path)

with open(cartoonization_log_path, 'r') as cartoonization_log_file:
    msg = 'Reading the cartoonization log file to match each image to the method used...'
    print(msg), logger.info(msg)
    lines = iter(cartoonization_log_file.readlines())
    for line in tqdm(lines):
        if '../data/groundtruth_images\\' in line: # were the image name appears
            image_name = line.split(',')[0].split('\\')[-1]
            msg = f'Reading image {image_name}'
            logger.info(msg)
            next_line = next(lines) # to know which method were used to cartoonize

            if next_line.split()[-2]: # if 'Using' is the second to last word on the next line, then the next one is (hopefully) the method name:
                method = next_line.split()[-1]
                msg = f'Method used {method}'
                logger.info(msg)
                methods_used.append({'image_name': image_name, 'method': method}) # math the image to the cartoonization method used
msg = f'Done'
print(msg), logger.info(msg)

# Retrieve the cartoonization methods defined in the cartoonizer_methods module
msg = 'Retrieving the cartoonization methods defined in the cartoonizer_methods module...'
print(msg), logger.info(msg)

import cartoonization_methods
methods = [element for element in dir(cartoonization_methods) if callable(getattr(cartoonization_methods, element))]
msg = 'Done'
print(msg), logger.info(msg)

# Create directories (or empty them if they exist) containing cartoonized images per method
data_dir = os.path.join(current_dir, '../data') # where the directories are going to be created

msg = 'Preparing directories to contain cartoonized images per method...'
print(msg), logger.info(msg)

for cartoonization_method in methods:
    method_dir = 'cartoonized_with_' + cartoonization_method
    method_dir = os.path.join(data_dir, method_dir)
    create_if_not_exist_or_delete_everything_inside(method_dir, log_file_path=log_file_path)
    
    # Once the directory created or emptied, fill it with corresponding images
    method_images = [method_used['image_name'] for method_used in methods_used if method_used['method'] == cartoonization_method]
    src = os.path.join(data_dir, 'cartoonized_images') # take images from the carrtoonized ones
    dst = method_dir # copy them into method_dir

    msg = 'Copying images to their transformation methods folder...'
    print(msg), logger.info(msg)
    
    for image in tqdm(method_images):
        shutil.copy(os.path.join(src, image), dst)

    msg = 'Done'
    print(msg), logger.info(msg)

# End
end = time() - start
msg = f'Split by cartoonization method finished in {end}s'
print(msg), logger.info(msg)