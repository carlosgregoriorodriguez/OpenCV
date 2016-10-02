# -*- coding: utf-8 -*-
from astropy.io import fits
import sys
import cv2
import numpy as np

fitsFileI="../examples/Filters/frame-i-004264-4-0259.fits" #m81 http://mirror.sdss3.org/fields/name?name=m81
fitsFileI2="../examples/Filters/frame-i-003804-6-0084.fits" #m66 http://mirror.sdss3.org/fields/name?name=m66
fitsFileI3='../examples/Filters/frame-i-004381-2-0120.fits' #m91 http://mirror.sdss3.org/fields/name?name=m91
fitsFileI4='../examples/Filters/frame-i-002830-6-0398.fits' #m109 http://mirror.sdss3.org/fields/name?name=m109
fitsFileI5='../examples/Filters/frame-i-003805-2-0023.fits' #m59 http://mirror.sdss3.org/fields/name?name=m59
fitsFileI6='../examples/Filters/frame-i-008112-2-0074.fits' #m33 http://mirror.sdss3.org/fields/name?name=m33
fitsFileI7='../examples/Filters/frame-i-007845-2-0104.fits' #m74 http://mirror.sdss3.org/fields/name?name=m74
fitsFileI8='../examples/Filters/frame-i-003836-4-0084.fits' #m95 http://mirror.sdss3.org/fields/name?name=m95
dataset={'i':fitsFileI,'i2':fitsFileI2,'i3':fitsFileI3,'i4':fitsFileI4,'i5':fitsFileI5,'i6':fitsFileI6,'i7':fitsFileI7,'i8':fitsFileI8}

hdu_list = fits.open(dataset[sys.argv[1]])
img = hdu_list[0].data

Min=np.amin(img)
Max=np.amax(img)
img = 255*(img+abs(Min))/Max
imgFiltered=cv2.filter2D(img,-1,np.array([[0,1,0],[1,0,1],[0,1,0]]))
_,imgBase=cv2.threshold(imgFiltered, cv2.THRESH_OTSU, 0, cv2.THRESH_TOZERO_INV)

imgProcessed=cv2.morphologyEx(imgBase, cv2.MORPH_CLOSE, (3,3),iterations=5)

cv2.namedWindow("Base image",cv2.WINDOW_NORMAL)
cv2.imshow("Base image", imgProcessed)
cv2.imwrite("imgClose.png",255*imgProcessed)
cv2.waitKey(0)



#Código basado en el manual https://www.learnopencv.com/blob-detection-using-opencv-python-c/

im = cv2.imread("imgClose.png") #Carga de la imagen generada aplicando la operación cierre

#Creación del contenedor de los parámetros
params = cv2.SimpleBlobDetector_Params()

#Filtrado por convexidad
params.filterByConvexity = True
params.minConvexity = 0.5
#Filtrado por elongación
params.filterByInertia = True
params.minInertiaRatio = 0.1

#Creación del detector con los parámetros fijados
detector = cv2.SimpleBlobDetector(params)

#Detección de los blobs
keypoints = detector.detect(im)

#La siguiente función marca con una circunferencia los blolbs detectados
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
cv2.namedWindow("Keypoints",cv2.WINDOW_NORMAL)
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
