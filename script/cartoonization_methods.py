import logging
import cv2

# Create and configure logger
logging.basicConfig(filename='../logs/cartoonization.log',
                    format='%(asctime)s %(lineno)d %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

logger.info('Defining cartoonization methods')

def method_1(image):
    logger.info('Cartoonizing using method 1')

    try:
        # Grayscale the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply median blur to smoothen the image
        gray_blur = cv2.medianBlur(gray, 5)

        # Detect edges using adaptive thresholding
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        # Convert edges back to color
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Apply bitwise_and to merge the edges with the original image
        cartoon = cv2.bitwise_and(image, edges)
    except Exception as e:
        logger.info(e)
        return
    else:
        logger.info('Cartoonization using method 1 complete')    
        return cartoon

def method_2(image):
    logger.info('Cartoonizing using method 2')

    try:
        # Apply bilateral filter to smoothen the image while preserving edges
        bilateral_filtered_image = cv2.bilateralFilter(image, 7, 75, 75)

        # Convert image to grayscale
        gray_image = cv2.cvtColor(bilateral_filtered_image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding to extract edges
        edge_detected_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

        # Convert edges back to color
        edge_detected_image = cv2.cvtColor(edge_detected_image, cv2.COLOR_GRAY2BGR)

        # Apply bitwise_and to merge the edges with the original image
        cartoon_image = cv2.bitwise_and(bilateral_filtered_image, edge_detected_image)
        
        # Apply bilateral filter to smoothen the image while preserving edges
        bilateral_filtered_image = cv2.bilateralFilter(image, 7, 75, 75)

        # Convert image to grayscale
        gray_image = cv2.cvtColor(bilateral_filtered_image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding to extract edges
        edge_detected_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

        # Convert edges back to color
        edge_detected_image = cv2.cvtColor(edge_detected_image, cv2.COLOR_GRAY2BGR)

        # Apply bitwise_and to merge the edges with the original image
        cartoon = cv2.bitwise_and(bilateral_filtered_image, edge_detected_image)
    except Exception as e:
        logger.info(e)
        return
    else:
        logger.info('Cartoonization using method 2 complete')
        return cartoon