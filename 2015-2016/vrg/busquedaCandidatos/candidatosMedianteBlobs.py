# Standard imports
import cv2
import numpy as np;
import math

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
	e =  2.71828
	im = cv2.imread("miniSetEstrellayGalaxia.png", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im)
	index=0
	flux = np.zeros([len(keyPoints)])
	print flux
	for k in keyPoints:
		flux[index] = im.item(int(k.pt[1]), int(k.pt[0]))
		print "Punto: "+str(index)+" ("+str(int(k.pt[0]))+", "+str(int(k.pt[1]))+") with size :"+str(k.size)+ "and intensity: "+str(im.item(int(k.pt[1]), int(k.pt[0])))
		#if index<len(keyPoints)//2:
		cv2.putText(im,str(index), (int(k.pt[0]),int(k.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255)
		index = index + 1
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	print flux
	print "Umbral flujo estrellas: "+str((np.mean(flux)-np.amin(flux))/e)
	cv2.waitKey(0)

	im = cv2.imread("image_3417_1e-LEDA-1852.jpg", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im)
	index=0
	for k in keyPoints:
		print "Punto: "+str(index)+" ("+str(int(k.pt[0]))+", "+str(int(k.pt[1]))+") with size :"+str(k.size)+ "and intensity: "+str(im.item(int(k.pt[1]), int(k.pt[0])))
		if index<len(keyPoints)//2:
			cv2.putText(im,str(index), (int(k.pt[0]),int(k.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,0))
		index = index + 1
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	cv2.waitKey(0)

	im = cv2.imread("o-HUBBLE-UV-900.jpg", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im)
	index=0
	for k in keyPoints:
		print "Punto: "+str(index)+" ("+str(int(k.pt[0]))+", "+str(int(k.pt[1]))+") with size :"+str(k.size)+ "and intensity: "+str(im.item(int(k.pt[1]), int(k.pt[0])))
		if index<len(keyPoints)//2:
			cv2.putText(im,str(index), (int(k.pt[0]),int(k.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,0))
		index = index + 1
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	cv2.waitKey(0)
	
	print "##############tutifruti.png#############"
	im = cv2.imread("tutifruti.png", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im)
	index=0
	for k in keyPoints:
		print "Punto: "+str(index)+" ("+str(int(k.pt[0]))+", "+str(int(k.pt[1]))+") with size :"+str(k.size)+ "and intensity: "+str(im.item(int(k.pt[1]), int(k.pt[0])))
		#if index<len(keyPoints)//2:
		cv2.putText(im,str(index), (int(k.pt[0]),int(k.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,0))
		index = index + 1
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	cv2.waitKey(0)
	
	im = cv2.imread("tutifrutiDesenfocado.png", cv2.IMREAD_GRAYSCALE)
	keyPoints = getIntersetObjectList(im)
	index=0
	for k in keyPoints:
		print "Punto: "+str(index)+" ("+str(int(k.pt[0]))+", "+str(int(k.pt[1]))+") with size :"+str(k.size)+ "and intensity: "+str(im.item(int(k.pt[1]), int(k.pt[0])))
		if index<len(keyPoints)//2:
			cv2.putText(im,str(index), (int(k.pt[0]),int(k.pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,0))
		index = index + 1
	resultado = cv2.drawKeypoints(im, keyPoints, np.array([]), (255,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Imagen Resultado", resultado)
	cv2.waitKey(0)
