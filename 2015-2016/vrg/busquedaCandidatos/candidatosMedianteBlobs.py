# Standard imports
import cv2
import numpy as np;
import math

# Read image

def getObjectList(img, minThreshold = 10, maxThreshold=255, debug=False):
	img = cv2.bitwise_not(img)
	params = cv2.SimpleBlobDetector_Params()
	params.minThreshold = minThreshold;
	params.maxThreshold = maxThreshold;
	params.filterByArea = 1
	params.minArea  = 3
	detector = cv2.SimpleBlobDetector_create(params)
	keyPoints = detector.detect(img)
	print "[getIntersetObjectList] hay un total de "+str(len(keyPoints))+" candidatos"
	index=0
	flux = np.zeros([len(keyPoints)])
	size = np.zeros([len(keyPoints)])
	for k in keyPoints:
		flux[index] = img.item(int(k.pt[1]), int(k.pt[0]))
		size[index] = k.size
		index = index + 1
	umbral = (np.mean(flux)-np.amin(flux))/np.e
	boxSize = (np.median(size))*np.pi
	print "Median (mediana) box size "+str(boxSize)
	index=0
	lCandidatos = np.zeros(0)
	height, width = img.shape
	blank_image = np.zeros((height, width, 1), np.uint8)
	for k in keyPoints:
		if img.item(int(k.pt[1]), int(k.pt[0]))>=umbral:
			if debug:
				print "Punto: "+str(index)+" ("+str(int(k.pt[0]))+", "+str(int(k.pt[1]))+") with size :"+str(k.size)+ "and intensity: "+str(img.item(int(k.pt[1]), int(k.pt[0])))
			cv2.circle(blank_image, (int(k.pt[0]),int(k.pt[1])), int(k.size), (255,0,0),-1)
			np.append( lCandidatos, [k.pt[0],k.pt[1], "Star"] )
		elif k.size>boxSize:
			if debug:
				print "\tPunto: "+str(index)+" ("+str(int(k.pt[0]))+", "+str(int(k.pt[1]))+") with size :"+str(k.size)+ "and intensity: "+str(img.item(int(k.pt[1]), int(k.pt[0])))+" descartado como estrella, quizas galaxia"
			np.append( lCandidatos, [k.pt[0],k.pt[1], "Galaxy or reject"] )
			resta = k.size/2.0
			cv2.rectangle(blank_image, (int(k.pt[0]-resta),int(k.pt[1]-resta)), (int(k.pt[0]+resta),int(k.pt[1]+resta)), 190,-1)
		else:
			np.append( lCandidatos, [k.pt[0],k.pt[1], "Galaxy or reject"] )
			resta = k.size/2.0
			cv2.rectangle(blank_image, (int(k.pt[0]-resta),int(k.pt[1]-resta)), (int(k.pt[0]+resta),int(k.pt[1]+resta)), 100,-1)
	return lCandidatos, blank_image


if __name__ == "__main__":
	raw_input("Se abriran dos imagenes, una con la imagen original y otra con un mapa de durezas que localiza las posibles estrellas y galaxias.\nPara pasar a la siguiente imagen a analizar, ha de tener el foco sobre una de las dos ventanas y pulsar cualquier tecla.\n")
	print "Two images will be open, the original and a 'durezas' image with info about star as circle and glaxies centers as grey rectangles"
	im = cv2.imread("tutifruti.png", cv2.IMREAD_GRAYSCALE)
	lista, imagen = getObjectList(im, debug=False)
	cv2.imshow("Mapa de durezas de estrellas", imagen)
	cv2.imshow("Original", im)
	cv2.waitKey(0)

	print "Two images will be open, the original and a 'durezas' image with info about star as circle and glaxies centers as grey rectangles"
	im = cv2.imread("o-HUBBLE-UV-900.jpg", cv2.IMREAD_GRAYSCALE)
	lista, imagen = getObjectList(im, debug=False)
	cv2.imshow("Mapa de durezas de estrellas", imagen)
	cv2.imshow("Original", im)
	cv2.waitKey(0)
	
	print "Two images will be open, the original and a 'durezas' image with info about star as circle and glaxies centers as grey rectangles"
	im = cv2.imread("image_3417_1e-LEDA-1852.jpg", cv2.IMREAD_GRAYSCALE)
	lista, imagen = getObjectList(im, debug=False)
	cv2.imshow("Mapa de durezas de estrellas", imagen)
	cv2.imshow("Original", im)
	cv2.waitKey(0)
	
	print "Two images will be open, the original and a 'durezas' image with info about star as circle and glaxies centers as grey rectangles"
	im = cv2.imread("tutifrutiDesenfocado.png", cv2.IMREAD_GRAYSCALE)
	lista, imagen = getObjectList(im, debug=False)
	cv2.imshow("Mapa de durezas de estrellas", imagen)
	cv2.imshow("Original", im)
	cv2.waitKey(0)


	'''
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
'''