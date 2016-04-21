"""
Created on Sun Jan 03 17:20:50 2016

working script - color detection

IMPLEMENTED: 
+blue color filter
+hsv 3-component splitting

@author: Dominik
"""
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,160,50])
    upper_blue = np.array([130,255,255])
    print lower_blue
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    
    h,s,v = cv2.split(res)
    
    cv2.imshow('gray',v)

    key = cv2.waitKey(5) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
 
cap.release()
cv2.destroyAllWindows()