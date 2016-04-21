# -*- coding: utf-8 -*-
"""
Created on Fri Jan 08 12:20:50 2016

testing script made for second, side camera - tracks the height distance between user's arm and a printed keyboard

IMPLEMENTED: 
+movement detection - implemented: color detection, hsv splitting and v-component extract
+cv2.findContours is used in extracting v-component (improved detection with blue color detection filter only)
+horizontal ground line implemented, horizontal ground coordinates and moving object coordinates catching
+check if letter typed implemented
+height distance and hit - distance between user's arm and printed keyboard - when distance is aprox 0, keystroke hit is detected

@author: Dominik
"""

import argparse
import datetime
import time
import cv2
import numpy as np


baseCoordPair = []
baseCoordA = (0,0)
baseCoordB = (0,0)
objectCoordA = (0,1000)
objectCoordB = (0,1000)

def on_mouse(event, x, y, flags, param):
	global baseCoordPair, baseCoordA, baseCoordB
	
	if event == cv2.EVENT_LBUTTONDOWN:
		print 'Start Mouse Position: '+str(x)+', '+str(y)
		startMouseCoord = (x,y)		
		baseCoordPair.append(startMouseCoord)
	
	elif event == cv2.EVENT_LBUTTONUP:
		print 'End Mouse Position: '+str(x)+', '+str(y)
		endMouseCoord = (x,y)	
		baseCoordPair.append(endMouseCoord)
		baseCoordA=(baseCoordPair[0])        
		baseCoordB=(baseCoordPair[1])            
		cv2.line(frame, baseCoordPair[0], baseCoordPair[1], (0,255,0), 2)
		cv2.imshow('edited', frame) 
		#multiple line draw
		#baseCoordPair[:]=[]

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

#minimum area size - minimum size of moving object
ap.add_argument("-a", "--min-area", type=int, default=2000, help="minimum area size")
args = vars(ap.parse_args())
 
# we are reading from webcam
camera = cv2.VideoCapture(1)
time.sleep(0.25)
  
# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the Typing/ Not typing text
	(grabbed, frame) = camera.read()
	text = "Not typing"
	cv2.imshow('image', frame) 
	cv2.setMouseCallback('image', on_mouse)
	
	# if the frame could not be grabbed, then we have reached the end of the video
	if not grabbed:
		break
	
	# Convert BGR to HSV
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  
   
	# define range of blue color in HSV
	lower_blue = np.array([110,160,50])
	upper_blue = np.array([130,255,255])
    
	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
	# Bitwise-AND mask and original image      	
	res = cv2.bitwise_and(frame,frame, mask = mask)   
    
	#cv2.imshow('frame',frame)
	#cv2.imshow('mask',mask)
	#cv2.imshow('res',res)
        
	h,s,gray = cv2.split(res)
 
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

      # compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	_,cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		objectCoordA=(x,y + h)
		objectCoordB=(x + w,y + h)
		#print objectCoordA, objectCoordB
		text = "Typing"
	
	#subtracting 10 so I could check value baseCoordA+-10, 20 numbers precision in a foor loop
	objectPosY=baseCoordA[1]
	objectPosY-=10
	
	#print baseCoordA, baseCoordB, baseCoordA[1], baseCoordB[1]
	#print objectPosY, baseCoordA, objectCoordA, objectCoordB
	
	#if objectCoordA[1] and objectCoordB[1] and baseCoordA[1] and baseCoordB[1]:
	#if objectCoordA[1] and objectCoordB[1]:		
	for i in range(0,20):
		objectPosY+=i
		if objectCoordA[1] == objectPosY or objectCoordB[1] == objectPosY:
			print "hit!"
			objectCoordA = (0,1000)
			objectCoordB = (0,1000)
  
      # draw the text and timestamp on the frame
	cv2.putText(frame, "Typing Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	cv2.imshow("Feed", frame)
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)
	
	key = cv2.waitKey(1) & 0xFF 
	# if the `q` key is pressed, break from the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
