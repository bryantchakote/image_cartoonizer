import os
import logging
import cv2
import inspect

# Current directory
current_dir = os.getcwd()

# Create and configure the logger
log_file_path = os.path.join(current_dir, '../logs/cartoonize.log')
logging.basicConfig(
    filename=log_file_path,
    filemode='w',
    format='%(asctime)s - %(filename)s line %(lineno)d - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger()

# Cartoonizer 1
def cartoonizer_1(image):
    logger.info(f'Using {inspect.currentframe().f_code.co_name}') # get the name of the running function

    try:
        ## Grayscale the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ## Apply median blur to smoothen the image
        gray_blur = cv2.medianBlur(gray, 5)

        ## Detect edges using adaptive thresholding
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        ## Convert edges back to color
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        ## Apply bitwise_and to merge the edges with the original image
        cartoon = cv2.bitwise_and(image, edges)
    except Exception as e:
        logger.error(e)
        return
    else:
        logger.info('Complete')    
        return cartoon

# Cartoonizer 2
def cartoonizer_2(image):
    logger.info(f'Using {inspect.currentframe().f_code.co_name}') # get the name of the running function

    try:        
        ## Apply bilateral filter to smoothen the image while preserving edges
        bilateral_filtered_image = cv2.bilateralFilter(image, 7, 75, 75)

        ## Convert image to grayscale
        gray_image = cv2.cvtColor(bilateral_filtered_image, cv2.COLOR_BGR2GRAY)

        ## Apply adaptive thresholding to extract edges
        edge_detected_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

        ## Convert edges back to color
        edge_detected_image = cv2.cvtColor(edge_detected_image, cv2.COLOR_GRAY2BGR)

        ## Apply bitwise_and to merge the edges with the original image
        cartoon = cv2.bitwise_and(bilateral_filtered_image, edge_detected_image)
    except Exception as e:
        logger.error(e)
        return
    else:
        logger.info('Complete')
        return cartoon

# If the module is correctly loaded
msg = 'Cartoonization methods loaded successfully'
print(msg), logger.info(msg)
