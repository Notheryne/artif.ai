import PIL
import pytesseract
import cv2
import numpy as np
import os

def ocr_core2(img_path):
    final_path = "./" + img_path
    img = cv2.imread(final_path)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
##########################################################################################
    print("I'm here!!!")
    # Rescale the image, if needed.
    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    print("I'm here1")
    # Load the aerial image and convert to HSV colourspace
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    print("I'm here2")
    # Define lower and uppper limits of what we call "brown"
    white_lo=np.array([0,0,170])
    white_hi=np.array([255,80,255])
    print("I'm here3")
    # Mask image to only select browns
    mask=cv2.inRange(hsv,white_lo,white_hi)
    #
    print("I'm here4")
    img[mask>0]=(0,0,0)
    img[mask==0]=(0,255,0)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    print("I'm here5")
    img = cv2.GaussianBlur(img, (5, 5), 1)
    #img = cv2.medianBlur(img,7)
    print("I'm here6")
##########################################################################################

    # Recognize text with tesseract for python
    text = pytesseract.image_to_string(img, lang = 'eng')
    print("I'm here7")
    return text
