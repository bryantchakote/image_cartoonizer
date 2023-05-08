import os
import logging
from time import time
import sys
import shutil

# Default log file
current_dir = os.getcwd()
log_file_path = os.path.join(current_dir, '../logs/untracked.log')

def create_if_not_exist_or_delete_everything_inside(folder_path, log_file_path=log_file_path):
    """
    This function takes a folder path and a log file path as arguments and:
    - creates the folder if it doesn't exist,
    - empty it otherwise.

    The log file path specifies where to write the logs when this function is called.
    """

    # Log file concerns
    logging.basicConfig(
        filename=log_file_path,
        filemode='a',
        format='%(asctime)s - %(filename)s line %(lineno)d - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    logger = logging.getLogger()

    # Start
    start = time()
    msg = f'utils.create_if_not_exist_or_delete_everything_inside running...'
    print(msg), logger.info(msg)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        msg = f'Folder {folder_path} not found'
        print(msg), logger.info(msg)
        msg = 'Creating it...'
        print(msg), logger.info(msg)
        try:
            os.makedirs(folder_path)
            msg = f'Folder {folder_path} created successfully within {time() - start}s'
            print(msg), logger.info(msg)
        except Exception as e:
            print(e), logger.error(e)
            sys.exit()
    # Delete everything inside it otherwise
    else:
        msg = f'Folder {folder_path} already exists'
        print(msg), logger.info(msg)
        msg = 'Emptying it...'
        print(msg), logger.info(msg)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                msg = f'Failed to delete {file_path}. Reason: {e}'
                print(msg), logger.error(msg)
                sys.exit()
        msg = f'Deletion done within {time() - start}s'
        print(msg), logger.info(msg)
