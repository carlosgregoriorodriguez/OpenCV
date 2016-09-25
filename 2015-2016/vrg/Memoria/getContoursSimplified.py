def getContours(imOrig, maxContours=10, t1=200, maxCtNumber = 1000):
	maxC = maxContours
	nContour = 0
	lastContours = 0
	contours = []
	while ((2*lastContours>=nContour) and maxC>0):
		im = dilate(closeContour(imOrig, maxC-1),(maxC+1)/2)
		imgray = im
		ret,thresh = cv2.threshold(imgray,t1,255,0)
		lastContours = nContour		
		nContour = len(contours)
		if (lastContours == 0):#caso 0
			lastContours = nContour	
		maxC=maxC-1
	epsilon = 10
	contours=[cv2.approxPolyDP(ctn,epsilon,True)for ctn in contours]
	area = np.zeros(len(contours))
	isParent = np.zeros(len(contours))

	index = 0
	for cnt in contours:
		if (hierarchy[[0],[index],[3]]==-1):
			isParent[index]=1
		area[index] = cv2.contourArea(cnt)
		index=index+1
	meanArea = np.mean(area)
	isSubContour = np.where(isParent==0)
	if (len(contours)>maxCtNumber):
		toDelete = np.where(area<=.5*meanArea)
	else:
		toDelete = np.where(area<=.05* meanArea)
	goodContours = np.delete(contours, toDelete)
	return goodContours, meanArea