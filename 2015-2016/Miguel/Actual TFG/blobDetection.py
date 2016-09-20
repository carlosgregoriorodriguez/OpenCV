# -*- coding: utf-8 -*-
from astropy.io import fits
import cv2
import numpy as np

fitsFile="../TFG/frame-i-002830-6-0398.fits"
hdulist = fits.open(fitsFile)
img = hdulist[0].data

Min=np.amin(img)
Max=np.amax(img)
img = 255*(img+abs(Min))/Max
imgFiltered=cv2.filter2D(img,-1,np.array([[0,1,0],[1,0,1],[0,1,0]]))
_,imgBase=cv2.threshold(imgFiltered, cv2.THRESH_OTSU, 0, cv2.THRESH_TOZERO_INV)

imgProcessed=cv2.morphologyEx(imgBase, cv2.MORPH_CLOSE, (3,3),iterations=5)

#cv2.imwrite("img4.png",imgProcessed)


#Código basado en el manual https://www.learnopencv.com/blob-detection-using-opencv-python-c/

im = cv2.imread("img4.png") #Carga de la imagen generada aplicando la operación cierre

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
cv2.imwrite('BLOBTEST.png', im_with_keypoints)
cv2.waitKey(0)
