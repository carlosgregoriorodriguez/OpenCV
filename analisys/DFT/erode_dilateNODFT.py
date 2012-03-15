from utils import *
import cv2
import cv2.cv as cv
import numpy as np

if __name__ == "__main__":
    debug = False
    camera =  cv2.VideoCapture(0)
        
    func_names = ['erode','dilate']
    
    for name in func_names:
        createTestFrame(name,parameters[name])
    while 1:
        img = cv2.pyrDown(getFrame(camera,grayscale=True))

        cv2.imshow("original",cv2.pyrDown(img))
        for name in func_names:
            test(name,img,eval("cv2."+name),parameters[name])
        InputKey(camera)        
