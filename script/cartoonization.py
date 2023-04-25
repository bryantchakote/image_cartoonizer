from time import time
import logging
import os
import sys
import shutil
from natsort import natsorted
import cv2
import random
from cartoonization_methods import cartoonizer_1, cartoonizer_2

# Start
start = time()

# Create and configure the logger
logging.basicConfig(
    filename='../logs/cartoonization.log',
    filemode='w',
    format='%(asctime)s - %(filename)s line %(lineno)d - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger()

# Access the images folder
msg = 'Accessing the images folder...'
print(msg), logger.info(msg)

current_dir = os.getcwd()
images_dir = '../data/renamed_images'
data_dir = os.path.join(current_dir, images_dir)

if os.path.exists(data_dir):
    msg = 'Successfully accessed ' + data_dir
    print(msg), logger.info(msg)
else:
    msg = data_dir + ' not found'
    print(msg), logger.error(msg)
    sys.exit()

# Cartoonize the images
msg = 'Starting cartoonizing...'
print(msg), logger.info(msg)
msg = 'Creating the transformed images folder...'
print(msg), logger.info(msg)

## Transformed images folder
transformed_images_dir = '../data/transformed_images'
transformed_data_dir = os.path.join(current_dir, transformed_images_dir)

### Create the folder if it doesn't exist
if not os.path.exists(transformed_data_dir):
    try:
        os.makedirs(transformed_data_dir)
        msg = transformed_images_dir + ' created successfully'
        print(msg), logger.info(msg)
    except Exception as e:
        print(e), logger.error(e)
        sys.exit()
### Delete everything inside it otherwise
else:
    msg = f'Folder {transformed_images_dir} already exist'
    print(msg), logger.info(msg)
    msg = 'Emptying it'
    print(msg), logger.info(msg)
    for filename in os.listdir(transformed_data_dir):
        file_path = os.path.join(transformed_data_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            msg = f'Failed to delete {file_path}. Reason: {e}'
            print(msg), logger.error(msg)
            sys.exit()
    msg = 'Done'
    print(msg), logger.info(msg)

## Cartoonification process
for image_file in natsorted(os.listdir(data_dir)):    
    ### Read the image
    image_path = os.path.join(data_dir, image_file)
    try:
        image = cv2.imread(image_path)
    except Exception as e:
        print(e), logger.error(e)
    else:
        if image is not None:
            logger.info(f'{image_path}, loaded successfully')
            ### Choose a method and use it
            try:
                cartoonizer = random.choice([cartoonizer_1, cartoonizer_2])
                cartoon = cartoonizer(image)
            except Exception as e:
                print(e), logger.error(e)
            else:
                try:
                    ### Convert the BGR image to RGB
                    cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
                except Exception as e:
                    print(e), logger.error(e)
                else:
                    ### Save the cartoonized image
                    transformed_path = os.path.join(transformed_data_dir, image_file)
                    try:
                        cv2.imwrite(transformed_path, cartoon)
                        logger.info(f'Cartoonized image saved to {transformed_path}')
                    except Exception as e:
                        print(e), logger.error(e)
        else:
            msg = f'{image_path} couldn\'t be read'
            print(msg), logger.error(msg)

# End
end = time() - start
msg = f'Cartoonization finished in {end}s'
print(msg), logger.info(msg)
