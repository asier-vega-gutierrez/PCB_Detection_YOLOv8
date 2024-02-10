import cv2
import numpy as np


'''Metodo para rescalar imagenes'''
def rescale_image(img, scale_percent):

    # Get the original width and height
    original_width, original_height = img.shape[1], img.shape[0]

    # Calculate the new width and height based on the scale percentage
    new_width = int(original_width * scale_percent / 100)
    new_height = int(original_height * scale_percent / 100)

    # Resize the image
    resized_image = cv2.resize(img, (new_width, new_height))

    return resized_image

'''Metodo para sber si una box esta dentor de otra'''
def is_inside_box(big_box, small_box):
    x1_big, y1_big, x2_big, y2_big = big_box
    
    x1_small, y1_small, x2_small, y2_small = small_box
    if (x1_big <= x1_small and y1_big <= y1_small and
        x2_big >= x2_small and y2_big >= y2_small):
        return True
    
    return False

'''Metodo para contar el numero de numeros de una lista'''
def count_occurrences(lst):
    counts = {}
    for num in lst:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1
    return counts