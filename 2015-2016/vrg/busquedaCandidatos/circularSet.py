# Standard imports
import cv2
import numpy as np

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
	
im = cv2.imread("miniSetEstrellayGalaxia.png", cv2.IMREAD_GRAYSCALE)
keyPoints = getIntersetObjectList(im)
print "Punto y coordenada:"
print str(type(keyPoints))
resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
resultado = im
#for item in keyPoints:
	#print str(item.pt[0])+", "+str(item.pt[1])
	#cv2.circle(resultado, (int(item.pt[0]),int(item.pt[1])), 5, (255,255,0))
print "Tomamos el primero"
print str(keyPoints[0].pt[0])+", "+str(keyPoints[0].pt[1])
for i in range(1, 64, 1):
	re = cutImage(im, keyPoints[0],i)
	mediaImg = cv2.mean(re)[0]
	print "Media de la imagen["+str(i)+"] "+str(mediaImg)

re = cutImage(im, keyPoints[0],10)
cv2.imshow("Imagen Resultado", re)
cv2.waitKey(0)