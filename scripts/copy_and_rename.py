from time import time
import os
import logging
from utils import create_if_not_exist_or_delete_everything_inside
from tqdm import tqdm
from natsort import natsorted
import shutil

# Start
start = time()

# Current directory
current_dir = os.getcwd()

# Create and configure the logger
log_file_path = os.path.join(current_dir, '../logs/copy_and_rename.log')
logging.basicConfig(
    filename=log_file_path,
    filemode='w',
    format='%(asctime)s - %(filename)s line %(lineno)d - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger()

# Source and destination directories
src_dir = os.path.join(current_dir, '../data/original_images')
dest_dir = os.path.join(current_dir, '../data/groundtruth_images')

# Create the destination directory or empty it
create_if_not_exist_or_delete_everything_inside(dest_dir, log_file_path=log_file_path)

# Iterate through all the files in the source directory and rename them
msg = 'Copying and renaming the images...'
print(msg), logger.info(msg)
i = 1
for filename in tqdm(natsorted(os.listdir(src_dir))):
    new_filename = str(i) + '.jpg'
    try:
        shutil.copy(os.path.join(src_dir, filename), os.path.join(dest_dir, new_filename))
    except Exception as e:
        print(e), logger.info(e)
    i += 1

# End
end = time() - start
msg = f'Copy and rename finished within {end}s'
print(msg), logger.info(msg)
