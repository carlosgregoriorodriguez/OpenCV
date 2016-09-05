# Standard imports
import cv2
import numpy as np;
 
# Read image

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

if __name__ == "__main__":
	print "Ejecutando getIntersetObjectList sobre una serie de 6 imagenes"

	im = cv2.imread("miniSetEstrellayGalaxia.png", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im)
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	cv2.waitKey(0)
	
	im = cv2.imread("image_3417_1e-LEDA-1852.jpg", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im)
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	cv2.waitKey(0)

	im = cv2.imread("o-HUBBLE-UV-900.jpg", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im)
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	cv2.waitKey(0)
	
	im = cv2.imread("noReal2.jpg", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im,190)
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	cv2.waitKey(0)
	
	im = cv2.imread("tutifruti.png", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im)
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	cv2.waitKey(0)
	
	im = cv2.imread("tutifrutiDesenfocado.png", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im)
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	cv2.waitKey(0)