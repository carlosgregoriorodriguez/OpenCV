#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import sys
import cv2
import math

gl_S = 169
gl_V = 114
gl_R = 134
gl_G= 94
gl_B = 0
frame_pos = 930
angles = []
cont_angles = 0
def onTrackbarSlideS(img,pos):
        global gl_S
        gl_S = pos
        process(img)
def onTrackbarSlideV(img,pos):
        global gl_V
        gl_V = pos
        process(img)
def onTrackbarSlideR(img,pos):
        global gl_R
        gl_R = pos
        process(img)
def onTrackbarSlideG(img,pos):
        global gl_G
        gl_G = pos
        process(img)
def onTrackbarSlideB(img,pos):
        global gl_B
        gl_B = pos
        process(img)

def show(img):
    p = int(vid.get(cv2.cv.CV_CAP_PROP_POS_MSEC))
    cv2.putText(img,str(p/1000.0),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
    cv2.imshow("ori",img)
    
def onTrackbarSlidePos(pos):
    global vid, img
    vid.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos)
    f,img = vid.read()
    show(img)
    
def createBars(window,img):
    cv2.createTrackbar("S",window,gl_S,255,lambda pos: onTrackbarSlideS(img,pos))
    cv2.createTrackbar("V",window,gl_V,255,lambda pos: onTrackbarSlideV(img,pos))
    cv2.createTrackbar("R",window,gl_R,255,lambda pos: onTrackbarSlideR(img,pos))
    cv2.createTrackbar("G",window,gl_G,255,lambda pos: onTrackbarSlideG(img,pos))
    cv2.createTrackbar("B",window,gl_B,255,lambda pos: onTrackbarSlideB(img,pos))
    
def filter_high(img, value):
    img = cv2.inRange(img,lowerb=value,upperb=255)
    return img

def module(u):
    return math.sqrt(u[0]*u[0] + u[1]*u[1])
    
def angle(u, v):
    prod = u[0]*v[0] + u[1]*v[1]
    cos_ang = prod / (module(u)*module(v))
    ang = math.pi - math.acos(cos_ang)
    return 180*ang / math.pi
    
def show_contours(contours):
    cv2.rectangle(img,(50,115),(600,65),(0,64,0),cv2.cv.CV_FILLED)
    if len(contours)==3:
        p = []
        colors = [(255,0,0),(0,255,0), (0,0,255)]
        i = 0
        for c in contours:
            m = cv2.moments(c)
            x = int(roi[0][0] + m["m10"]/m["m00"])
            y = int(roi[0][1] +m["m01"]/m["m00"])
            cv2.circle(img, (x,y), 10, colors[i], 2) 
            i += 1
            p.append((x,y))
        
        cv2.line(img, p[0], p[1], (255,0,0), 1,cv2.cv.CV_AA)
        cv2.line(img, p[1], p[2], (255,0,0), 1,cv2.cv.CV_AA)
        v = (p[1][0]-p[0][0], p[1][1]-p[0][1]) 
        u = (p[2][0]-p[1][0], p[2][1]-p[1][1]) 
        alpha = angle(u,v)
        angles.append(alpha)
        cv2.putText(img,"{0:.2f}".format(alpha),(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
     
    
def process(imgroi):
    global img

    cv2.imshow("roi",imgroi)
    imgB, imgG, imgR = cv2.split(imgroi) 
    cv2.cvtColor(imgroi, cv2.COLOR_RGB2HSV);
    imgHSV = cv2.cvtColor(imgroi, cv2.COLOR_RGB2HSV)
    imgH, imgS, imgV = cv2.split(imgHSV) 
    filteredS = filter_high(imgS,gl_S)
    filteredV = filter_high(imgV,gl_V)
    filteredG = filter_high(imgG,gl_R)
    filteredR = filter_high(imgR,gl_G)
    filteredB = filter_high(imgB,gl_B)
    res = cv2.bitwise_and(filteredS,filteredV)
    res = cv2.bitwise_and(res,filteredG)
    res = cv2.bitwise_and(res,filteredR)
    res = cv2.bitwise_and(res,filteredB)
    res = cv2.blur(res,(5,5))
    res1 = res.copy()
    contours, hierarchy = cv2.findContours(res,cv2.cv.CV_RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_SIMPLE)
    show_contours(contours)
    
    cv2.imshow("ori",img)
    cv2.imshow("res",res)
    cv2.imshow("res1",res1)

    

    
def create_process_window(img):
    window_name = "res"    
    cv2.namedWindow(window_name)
    createBars(window_name,img)
    process(img)
    cv2.waitKey(-1)
    cv2.destroyWindow(window_name)
    
roi=[[544, 215], [792, 662]] 

def on_mouse(event, x, y, flags, param):
    global roi
    if event == cv2.cv.CV_EVENT_LBUTTONDOWN:
        roi[0]=[x,y]
    elif event == cv2.cv.CV_EVENT_LBUTTONUP:
        roi[1]=[x,y]
    
    
def main():
        global vid,roi, img
        
        vid = cv2.VideoCapture(sys.argv[1])
        cv2.namedWindow("ori")
        #frame_count = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        #cv2.createTrackbar("pos","ori",930,frame_count,onTrackbarSlidePos)
        #vid.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_count)
        cv2.setMouseCallback("ori",on_mouse)
        f,img = vid.read()

        while f:
                if roi==None:
                        roi=[[0,0],img.shape[:2]]
                imroi = img[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
                process(imroi)
                k = cv2.waitKey (1)
                if k == 27:
                        break
                f,img = vid.read()
                        
        cv2.destroyAllWindows()

        i = 0
        while i<len(angles):
                print i, "{0:,}".format(angles[i])
                i+=1
                
                
if __name__ == "__main__": 
    main()
