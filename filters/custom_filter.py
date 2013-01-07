#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import numpy
import sys

"""Estudiando la aplicación de filtros propios aparece el problema de las
 imágenes descritas con números reales. El script muestra la aplicación
 de un filtro creado con un kernel (y la convolución correspondiente) y
 sobre como manejar la imagen obtenida por dicho filtro, que habitualmente 
 tendrá unos valores poco relacionados con la representación de la imagen.

 Cambiar de filtro para ver las diferencias tan grandes en filtros tan pequeños.
"""

def img_properties(img,description=None):
    if description:
        print description.upper(), "......................."
    print type(img)
    print img.dtype
    print img.shape
    #print img   
    print cv2.minMaxLoc(img)

if __name__ == "__main__":
    img_in = cv2.imread(sys.argv[1],0)
    img_properties(img_in,"original")
    cv2.imshow("ORIGINAL",img_in)
    
    kernel = numpy.array([[1,0,-1],[1,0,-1],[1,0,-1]],numpy.float32)
    #kernel = kernel.transpose()    
    #kernel = numpy.array([[0,-1,0],[-1,4,-1],[0,-1,0]],numpy.float32)
    #kernel = numpy.array([[1,0,1],[0,-3,0],[1,0,1]],numpy.float32)
    img_properties(kernel,"kernel")

    img_out = cv2.filter2D(img_in, cv2.CV_32F, kernel)
    img_properties(img_out,"raw filtered image")
    cv2.imshow("RAW FILTERED", img_out)
    
    filter_1 = cv2.convertScaleAbs(img_out)
    img_properties(filter_1,"filtered convertScaleAbs")
    cv2.imshow("ConvertScaleAbs", filter_1)
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(img_out)
    img_out = (img_out+abs(min_val))/(abs(min_val)+max_val)
    img_properties(img_out,"filtered scaled with max min values")
    cv2.imshow("Scaled Min Max",img_out)
    cv2.imshow("convertScaleAbs scaled min max",cv2.convertScaleAbs(img_out,alpha=255))
    cv2.imshow("Canny", cv2.Canny(cv2.convertScaleAbs(img_out,alpha=255),100,200))
    convolution = cv2.flip(kernel,-1)
    img_properties(convolution,"convolution")

    img_conv = cv2.filter2D(img_in, cv2.CV_32F, convolution)
    img_properties(img_conv,"raw convolutioned")
    cv2.imshow("CONVOLVED",img_conv)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(img_conv)
    img_properties(img_conv,"convolutioned scaled with max min values")
    cv2.imshow("Convolved Scaled Min Max",(img_conv+abs(min_val))/(abs(min_val)+max_val))

    #cv2.imshow("black", numpy.zeros((300,400), dtype=numpy.float32))
    #cv2.imshow("white", numpy.ones((300,400), dtype=numpy.float32))
    #cv2.imshow("gray", numpy.ones((300,400), dtype=numpy.float32)*0.5)

    
    cv2.waitKey(0)
