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

'''Metodo para sacar la precision de cada componente'''
def component_accuracy(dict1, dict2):
    component_accuracies = {}
    for component in dict1:
        if component in dict2:
            quantity1 = dict1[component]
            quantity2 = dict2[component]
            accuracy = (quantity1 / quantity2)
            component_name = id_to_name(component, True)
            component_accuracies[component_name] = "{:.2f}".format(abs(accuracy))
    return component_accuracies

'''Metodo para cabiar de id a string'''
def id_to_name(id, component):
    if component == False:
        if id == 0:
            return 'ARDUINO_MEGA'
        elif id == 1:
            return 'ESP32'
        elif id == 2:
            return 'L298N'
        elif id == 3:
            return 'ULN2003'
        else:
            return None
    else:
        if id == 0:
            return 'IC'
        elif id == 1:
            return 'LED'
        elif id == 2:
            return 'BATTERY'
        elif id == 3:
            return 'BUZZER'
        elif id == 4:
            return 'CAPACITOR'
        elif id == 5:
            return 'CLOCK'
        elif id == 6:
            return 'CONNECTOR'
        elif id == 7:
            return 'DIODE'
        elif id == 8:
            return 'DISPLAY'
        elif id == 9:
            return 'FUSE'
        elif id == 10:
            return 'INDUCTOR'
        elif id == 11:
            return 'POTENTIOMETER'
        elif id == 12:
            return 'RELAY'
        elif id == 13:
            return 'RESISTOR'
        elif id == 14:
            return 'SWITCH'
        elif id == 15:
            return 'TRANSISTOR'
        else:
            return None