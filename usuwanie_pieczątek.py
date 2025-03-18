import cv2
import numpy as np

def usuń_pieczątkę(image):
    if image is None:
        print(f'Nie można wczytać obrazu')
        exit()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_gray = np.array([0, 0, 40])
    upper_gray = np.array([180, 50, 220])
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    mask = cv2.bitwise_or(mask_gray, mask_black)
    mask_inv = cv2.bitwise_not(mask)
    background = np.ones_like(image, dtype=np.uint8) * 255
    result = image.copy()
    result[mask_inv != 0] = [255, 255, 255]
    return result
    