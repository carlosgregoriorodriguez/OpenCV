import cvSpace
import cv2

print "HOla"

baseImage = cv2.imread('testMask.png',0)
contornos = cvSpace.getContours(baseImage)
print "NContornos "+str(len(contornos))
height, width = baseImage.shape
index = 8 
print contornos[index]
maskContour = cvSpace.getMaskFromContour(contornos[index], width, height)
masquerade = cvSpace.maskImage(baseImage, maskContour)
cv2.imshow('imageMask',masquerade)
cv2.imshow('imageContour',maskContour)
cv2.imshow('baseImage',baseImage)
print cvSpace.getGalaxyCenter(masquerade)
cv2.waitKey(0)
#cv2.destroyAllWindows()