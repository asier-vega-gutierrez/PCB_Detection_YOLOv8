import cv2
import numpy as np

   
def rescale_image(img, scale_percent):

    # Get the original width and height
    original_width, original_height = img.shape[1], img.shape[0]

    # Calculate the new width and height based on the scale percentage
    new_width = int(original_width * scale_percent / 100)
    new_height = int(original_height * scale_percent / 100)

    # Resize the image
    resized_image = cv2.resize(img, (new_width, new_height))

    return resized_image
