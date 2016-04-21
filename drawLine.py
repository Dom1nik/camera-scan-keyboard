# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 20:36:29 2016

testing script for line drawing on captured camera frame

IMPLEMENTED:
+simple line on-click drawing(start/end point)

@author: Dominik
"""


from time import time
import cv2
import numpy as np
boxes = []
count = 0
groundA = (0,0)
groundB = (0,0)



def on_mouse(event, x, y, flags, param):
        # global img
        #t = time()
       
        if event == cv2.EVENT_LBUTTONDOWN:
             print 'Start Mouse Position: '+str(x)+', '+str(y)
             sbox = (x,y)
             boxes.append(sbox)
             # print count
             # print sbox

        elif event == cv2.EVENT_LBUTTONUP:
            print 'End Mouse Position: '+str(x)+', '+str(y)
            ebox = (x,y)
            boxes.append(ebox)
            
            groundA=(boxes[0])        
            groundB=(boxes[1])
           
            print groundA, groundB
            
            cv2.line(frame, boxes[0], boxes[1], (0,255,0), 2)
            cv2.imshow('edited', frame) 
            #k =  cv2.waitKey(0)
            
            #multiple line draw
            #boxes[:]=[]


#img = np.zeros((480,640,3), np.uint8)
#cv2.namedWindow('image')
#cv2.imshow('image', img)

cam = cv2.VideoCapture(1)

while(True): 
                
        (grabbed, frame) = cam.read()
        #count += 1   
        cv2.imshow('image', frame) 
        #cv2.imshow('edit', frame) 
        cv2.setMouseCallback('image', on_mouse)
         
        """if count < 50:
            if cv2.waitKey(33) == 27:
                cv2.destroyAllWindows()
                break
        elif count >= 50:
            if cv2.waitKey(0) == 27:
                cv2.destroyAllWindows()
                break
            count = 0"""
        if cv2.waitKey(5) & 0xff == ord('q'):
            break
        
cam.release()
cv2.destroyAllWindows()
    
        
        