#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2


if __name__ == "__main__":


    camera = cv2.VideoCapture(0)

    g,im = camera.read()

    print "shape "+str(im.shape)
    print "number of elements "+str(im.size)
    print "nsize "+str(im.ndim)
    print "strides "+str(im.strides)

    imShape = im.shape

    auxiliarIm = cv2.pyrDown(cv2.pyrDown(cv2.pyrUp(cv2.pyrUp(im))))
    cv2.imshow('A original-DDUU',im.__sub__(auxiliarIm))
    cv2.imshow('A DDUU-DDUU',auxiliarIm.__sub__(auxiliarIm))
    cv2.imshow('A DDUU-original',auxiliarIm.__sub__(im))
    cv2.imshow('A original-DDUU-original+DDUU',(im.__sub__(auxiliarIm)).__sub__(auxiliarIm.__sub__(im)))
        
    print "entrada del original "+str(im[100,100,1])
    print "entrada del auxiliar "+str(auxiliarIm[100,100,1])
    print "entrada del original-auxiliar "+str((im.__sub__(auxiliarIm))[100,100,1])
    print "entrada del auxiliar-original "+str((auxiliarIm.__sub__(im))[100,100,1])
    print "deberia ser 0 "+str((im.__sub__(auxiliarIm)).__sub__(auxiliarIm.__sub__(im))[100,100,1])


    #print "con valor absoluto"
    #print "entrada del original "+str(im[100,100,1])
    #print "entrada del auxiliar "+str(auxiliarIm[100,100,1])
    #print "entrada del original-auxiliar "+str(((im.__sub__(auxiliarIm)).__abs__())[100,100,1])
    #print "entrada del auxiliar-original "+str(((auxiliarIm.__sub__(im)).__abs__())[100,100,1])
    #print "deberia ser 0 "+str((((im.__sub__(auxiliarIm)).__sub__(auxiliarIm.__sub__(im))).__abs__())[100,100,1])

    
    while True:

        f,img = camera.read()

        auxIm = cv2.pyrDown(cv2.pyrDown(cv2.pyrUp(cv2.pyrUp(img))))

        cv2.imshow('original-DDUU',img.__sub__(auxIm))
        cv2.imshow('DDUU-DDUU',auxIm.__sub__(auxIm))
        cv2.imshow('DDUU-original',auxIm.__sub__(img))
        cv2.imshow('original-DDUU-original+DDUU',(img.__sub__(auxIm)).__sub__(auxIm.__sub__(img)))
        
        if (cv2.waitKey(5) != -1):  
            break   






