#Cargar una imagen desde un fichero FITS
from astropy.io import fits
fitsFile="../examples/Filters/frame-i-002830-6-0398.fits"
hdulist = fits.open(fitsFile)
img = hdulist[0].data

#Mostrar una imagen con OpenCV
import cv2
import numpy as np

Min=abs(np.amin(img)) #Se toma el valor absoluto porque por errores en el CCD pueden existir mediciones ligeramente erradas. En concreto, negativas muy cercanas a cero
Max=np.amax(img)
img = 255*(img+Min)/Max

cv2.namedWindow("Image", cv2.WINDOW_NORMAL) #Se crea una ventana "Image"
cv2.imshow("Image",img) #Se dibuja img en la ventana Image
cv2.waitKey() #Esta sentencia muestra la ventana hasta que se presiona una tecla
