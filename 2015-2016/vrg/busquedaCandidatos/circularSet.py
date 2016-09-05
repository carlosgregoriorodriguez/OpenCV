# Standard imports
import cv2
import numpy as np
import cvSpace


def getIntersetObjectList(img, minThreshold = 10, maxThreshold=255):
	img = cv2.bitwise_not(img)
	params = cv2.SimpleBlobDetector_Params()
	params.minThreshold = minThreshold;
	params.maxThreshold = maxThreshold;
	params.filterByArea = 1
	params.minArea  = 3
	detector = cv2.SimpleBlobDetector_create(params)
	candidato = detector.detect(img)
	print "[getIntersetObjectList] hay un total de "+str(len(candidato))+" candidatos"
	return candidato

def cutImage(img, center, r=32):
	#cv2.circle(img, (int(center.pt[0]),int(center.pt[1])), 10, (255,255,0))
	return img[int(center.pt[1]-r):int(center.pt[1]+r), int(center.pt[0]-r):int(center.pt[0]+r)]
	
#im = cv2.imread("miniSetEstrellayGalaxia.png", cv2.IMREAD_GRAYSCALE)
im = cv2.imread("o-HUBBLE-UV-900.jpg", cv2.IMREAD_GRAYSCALE)
im2 = im.copy()
print "Tipo de la imagen: "+str(type(im))
print "#############################"
sig_fract = 5
percent_fract = 0.01
skyMedian, nIter = cvSpace.sky_median_sig_clip(im, sig_fract, percent_fract, max_iter=200)
print "skeMedian: "+str(skyMedian) + " iterations: "+str(nIter)
print "#############################"

keyPoints = getIntersetObjectList(im)
print "Punto y coordenada:"
print str(type(keyPoints))
resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
resultado = im
#for item in keyPoints:
	#print str(item.pt[0])+", "+str(item.pt[1])
	#cv2.circle(resultado, (int(item.pt[0]),int(item.pt[1])), 5, (255,255,0))
print "Tomamos el primero"
cualStar = 1
print str(keyPoints[cualStar].pt[0])+", "+str(keyPoints[cualStar].pt[1])
for i in range(1, 64, 1):
	re = cutImage(im, keyPoints[cualStar],i)
	mediaImg = cv2.mean(re)[0]
	#print "Media de la imagen["+str(i)+"] "+str(mediaImg)

re = cutImage(im, keyPoints[cualStar],64)
cv2.imshow("Imagen Resultado", re)
cv2.waitKey(0)