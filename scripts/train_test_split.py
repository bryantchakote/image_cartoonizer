from time import time
import os
import logging
import sys
from utils import create_if_not_exist_or_delete_everything_inside
from tqdm import tqdm
from natsort import natsorted
import cv2
import random
import shutil

# Start
start = time()

# Current directory
current_dir = os.getcwd()

# Create and configure the logger
log_file_path = os.path.join(current_dir, '../logs/train_test_split.log')
logging.basicConfig(
    filename=log_file_path,
    filemode='w',
    format='%(asctime)s - %(filename)s line %(lineno)d - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger()

# Load the ground truth and cartoonized images
msg = f'Loading the ground truth and cartoonized images...'
print(msg), logger.info(msg)

groundtruth_images_dir = os.path.join(current_dir, '../data/groundtruth_images')
cartoonized_images_dir = os.path.join(current_dir, '../data/cartoonized_images')

## Stop if one of the previous is missing
if not (os.path.exists(groundtruth_images_dir) and os.path.exists(cartoonized_images_dir)):
    msg = 'ERROR: ground truth or cartoonized images directory not found'
    print(msg), logger.error(msg)
    sys.exit()

## Stop if one of theprevious is empty
if (len(os.listdir(groundtruth_images_dir)) == 0 or len(os.listdir(cartoonized_images_dir)) == 0):
    msg = 'ERROR: ground truth or cartoonized images directory is empty'
    print(msg), logger.error(msg)
    sys.exit()

msg = f'Done'
print(msg), logger.info(msg)

# Join the matching images and save the result into transformed_images
msg = f'Joining the matching images and save the result into transformed_images'
print(msg), logger.info(msg)

transformed_images_dir = os.path.join(current_dir, '../data/transformed_images')
create_if_not_exist_or_delete_everything_inside(transformed_images_dir)

SIZE = (256, 256) # single image size

msg = f'Joining...'
print(msg), logger.info(msg)
for groundtruth_image_path, cartoonized_image_path in tqdm(zip(natsorted(os.listdir(groundtruth_images_dir)), natsorted(os.listdir(cartoonized_images_dir)))):
    ## If the names aren't the same, continue
    if groundtruth_image_path != cartoonized_image_path:
        msg = f'Incoherent images; the groundtruth: {groundtruth_image_path} doesn\'t match the cartoonized: {cartoonized_image_path}'
        print(msg), logger.warning(msg)
    else:
        try:
            groundtruth_image = cv2.imread(os.path.join(groundtruth_images_dir, groundtruth_image_path))
            groundtruth_image = cv2.resize(groundtruth_image, SIZE)
            cartoonized_image = cv2.imread(os.path.join(cartoonized_images_dir, cartoonized_image_path))
            cartoonized_image = cv2.resize(cartoonized_image, SIZE)
            transformed_image = cv2.hconcat([groundtruth_image, cartoonized_image])
            cv2.imwrite(os.path.join(transformed_images_dir, groundtruth_image_path), transformed_image)

            msg = f'{os.path.join(transformed_images_dir, groundtruth_image_path)} writed successfully'
            logger.info(msg)
        except Exception as e:
            print(e), logger.warning(e)

msg = f'Done'
print(msg), logger.info(msg)

# Split the transformed images into train and test set
msg = 'Spliting the transformed images into train and test set...'
print(msg), logger.info(msg)

train_size = .8
n = len(os.listdir(transformed_images_dir))
indices = list(range(n))
random.shuffle(indices)
train_indices = indices[:int(train_size*n)]
test_indices = indices[int(train_size*n):]
logger.info(f'{n}, {len(train_indices)}, {len(test_indices)}')

## Train
msg = 'Train...'
print(msg), logger.info(msg)

train_dir = os.path.join(current_dir, '../data/train')
create_if_not_exist_or_delete_everything_inside(train_dir)

for index in tqdm(train_indices):
    src = os.path.join(transformed_images_dir, os.listdir(transformed_images_dir)[index])
    dst = os.path.join(train_dir, os.listdir(transformed_images_dir)[index])
    shutil.copyfile(src, dst)

msg = f'Done'
print(msg), logger.info(msg)

## Test
msg = 'Test...'
print(msg), logger.info(msg)

test_dir = os.path.join(current_dir, '../data/test')
create_if_not_exist_or_delete_everything_inside(test_dir)

for index in tqdm(test_indices):
    src = os.path.join(transformed_images_dir, os.listdir(transformed_images_dir)[index])
    dst = os.path.join(test_dir, os.listdir(transformed_images_dir)[index])
    shutil.copyfile(src, dst)

msg = f'Done'
print(msg), logger.info(msg)

# End
end = time() - start
msg = f'Train test split finished in {end}s'
print(msg), logger.info(msg)
