import numpy as np
import cv2
import math
from astropy.io import fits#no necesario, cvSpace solo trabaja con arrays de imagenes
'''
	Main references:
		Preparing Red-Green-Blue Images from CCD Data Lupton et all
			http://adsabs.harvard.edu/abs/2004PASP..116..133L
'''
print "Loaded cvSpace"
def segment(img, thresholdStart, thresholdEnd):
	height, width = img.shape
	print "[cvSpace]::segment: "+str(height)
	for w in range (width):
		for h in range (height):
			if ((img.item(h, w)<thresholdStart) or (img.item(h, w)>thresholdEnd)):
				img.itemset(h, w,255)
	return img

def binarice(img, threshold, inverse = False):
	height, width = img.shape
	print "binarice threshold: "+str(threshold)
	for w in range (width):
		for h in range (height):
			if (inverse == True):
				if ((img.item(h, w)<threshold)):
					img.itemset(h, w,0)			
			else:
				if ((img.item(h, w)>threshold)):
					img.itemset(h, w,255)
	return img
	
def medianize(img, posX, posY):
	#controlar las fronteras
	height, width = img.shape
	sum = 0
	nValues = 0
	startX = posX -4
	if (startX<0):
		startX = 0
	endX = posX+4
	if (endX>width):
		endX = width
	startY = posY -4
	if (startY<0):
		startY = 0	
	endY = posY + 4
	if (endY>height):
		endT = height
	print "Entorno ("+str(startX)+", "+str(startY)+") -> ("+str(endX)+", "+str(endY)+")"
	for w in range(startX, endX):
		for h in range(startY, endY):
			nValues = nValues +1
			sum = sum + img.item(h,w)
	print "Suma: "+str(sum)
	print "Valores atrapados" +str(nValues)
	print "medianize Value "+str(sum/nValues)

def preEqualizaFits(img):
	print "[cvSpace]::preEqualizeFits"
	height, width = img.shape
	minFlux = img.min()
	maxFlux = img.max()
	value = 255.0-maxFlux
	adjustScaleFlux = 255/maxFlux
	print "Ini Flux ["+str(minFlux)+", "+str(maxFlux)+"]"
	'''
	for w in range (width):
		for h in range (height):
			pixFlux = img.item(h,w)
			img.itemset(h, w,int((-minFlux+pixFlux)*adjustScaleFlux))
	'''
	img = (-minFlux+img)*adjustScaleFlux
	minFlux = img.min()
	maxFlux = img.max()
	print "Processed Flux ["+str(minFlux)+", "+str(maxFlux)+"]"
	return img
	
def linear(inputArray, scale_min=None, scale_max=None):
	print "[cvSpace]::linear"
	img=np.array(inputArray, copy=True)
	
	if scale_min == None:
		scale_min = img.min()
	if scale_max == None:
		scale_max = img.max()

	print "linear: scale_min = "+str(scale_min)+"   scale_max = "+str(scale_max)
	img.clip(min=scale_min, max=scale_max)
	img = 255.0*(img -scale_min) / (scale_max - scale_min)
	indices = np.where(img < 0)
	img[indices] = 0.0
	indices = np.where(img > 100)
	height, width = img.shape
	for w in range (width):
		for h in range (height):
			if (img.item(h,w)>100):
				print str(h)+","+str(w)+" = "+str(img.item(h,w))
	
	return img

	
def sqrt(inputArray, scale_min=None, scale_max=None):
	print "[cvSpace]::sqrt"
	img=np.array(inputArray, copy=True)
	
	if scale_min == None:
		scale_min = img.min()
	if scale_max == None:
		scale_max = img.max()

	img.clip(min=scale_min, max=scale_max)
	img = img - scale_min
	indices = np.where(img < 0)
	img[indices] = 0.0
	img = np.sqrt(img)
	img = 255.0*img / np.sqrt(scale_max - scale_min)
	height, width = img.shape
	'''
	for w in range (width/10):
		for h in range (height/10):
			#if (img.item(h,w)>100):
			print str(h)+","+str(w)+" = "+str(img.item(h,w))
	'''
	print img.max()
	return img

def log(inputArray, scale_min=None, scale_max=None):    
	print "[cvSpace]::log"
	img=np.array(inputArray, copy=True)
	
	if scale_min == None:
		scale_min = img.min()
	if scale_min<0:
		suma = scale_min
	
	if scale_max == None:
		scale_max = img.max()
	
	factor = np.log10(scale_max - scale_min)
	indices0 = np.where(img < scale_min)
	indices1 = np.where((img >= scale_min) & (img <= scale_max))
	indices2 = np.where(img > scale_max)
	img[indices0] = 0.0
	img[indices2] = 1.0
	try :
		img[indices1] = np.log10(img[indices1])/factor
	except :
		print "Error on math.log10 for ", (img[i][j] - scale_min)

	return 255.0*img

def power(inputArray, exponente=3.0, scale_min=None, scale_max=None):
	print "[cvSpace]::power"
	img=np.array(inputArray, copy=True)
	
	if scale_min == None:
		scale_min = img.min()
	if scale_max == None:
		scale_max = img.max()
	factor = 1.0 / np.pow(scale_max, exponente)
	img = img + scale_min
	print "Factor: "+str(factor)
	indices0 = np.where(img < scale_min)
	indices1 = np.where((img >= scale_min) & (img <= scale_max))
	indices2 = np.where(img > scale_max)
	img[indices0] = 0.0
	img[indices2] = 1.0
	img[indices1] = np.power((img[indices1] - scale_min), exponente)*factor

	return 255.0*img

def asinh(inputArray, scale_min=None, scale_max=None, noLinaridad=2.0):
	print "[cvSpace]::asinh"
	img=np.array(inputArray, copy=True)
	
	if scale_min == None:
		scale_min = img.min()
	if scale_max == None:
		scale_max = img.max()
	factor = np.arcsinh((scale_max - scale_min)/noLinaridad)
	indices0 = np.where(img < scale_min)
	indices1 = np.where((img >= scale_min) & (img <= scale_max))
	indices2 = np.where(img > scale_max)
	img[indices0] = 0.0
	img[indices2] = 1.0
	img[indices1] = np.arcsinh((img[indices1] - scale_min)/noLinaridad)/factor

	return 255.0*img

def histeq(inputArray, num_bins=256):
	print "[cvSpace]::histeq"
	img=np.array(inputArray, copy=True)
	print "[cvSpace]::histeq Step 1"
	# histogram equalisation: we want an equal number of pixels in each intensity range
	sortedDataIntensities=np.sort(np.ravel(img))	
	median=np.median(sortedDataIntensities)
	print "median: "+str(median)
	# Make cumulative histogram of data values, simple min-max used to set bin sizes and range
	dataCumHist=np.zeros(num_bins)
	minIntensity=sortedDataIntensities.min()
	print "Minimal intensity: "+str(minIntensity)
	maxIntensity=sortedDataIntensities.max()
	print "Maximal intensity: "+str(maxIntensity)
	histRange=maxIntensity-minIntensity
	print "Range: "+str(histRange)
	binWidth=histRange/float(num_bins-1)
	print "binWidth: "+str(binWidth)
	print "[cvSpace]::histeq Step 2"
	for i in range(len(sortedDataIntensities)):
		binNumber=int(math.ceil((sortedDataIntensities[i]-minIntensity)/binWidth))
		addArray=np.zeros(num_bins)
		onesArray=np.ones(num_bins-binNumber)
		onesRange=range(binNumber, num_bins)
		np.put(addArray, onesRange, onesArray)
		dataCumHist=dataCumHist+addArray
	print "[cvSpace]::histeq Step 3 Generating Cumulative Histogram"      
	idealValue=dataCumHist.max()/float(num_bins)
	idealCumHist=np.arange(idealValue, dataCumHist.max()+idealValue, idealValue)
    
	# Map the data to the ideal
	for y in range(img.shape[0]):
		for x in range(img.shape[1]):
		# Get index corresponding to dataIntensity
			intensityBin=int(math.ceil((img[y][x]-minIntensity)/binWidth))
            
	# Frontier Problem
	if intensityBin<0:
		intensityBin=0
	if intensityBin>len(dataCumHist)-1:
		intensityBin=len(dataCumHist)-1
        
	# Get the cumulative frequency corresponding intensity level in the data
	dataCumFreq=dataCumHist[intensityBin]
            
	# Get the index of the corresponding ideal cumulative frequency
	idealBin=np.searchsorted(idealCumHist, dataCumFreq)
	idealIntensity=(idealBin*binWidth)+minIntensity
	img[y][x]=idealIntensity

	scale_min = img.min()
	scale_max = img.max()
	img.clip(min=scale_min, max=scale_max)
	img = (img -scale_min) / (scale_max - scale_min)
	indices = np.where(img < 0)
	img[indices] = 0.0
        
	return 255*img

#Helper functions	
def range_from_percentile(input_arr, low_cut=0.25, high_cut=0.25):
	print "[cvSpace]::range_from_percentile"
	work_arr = np.ravel(input_arr)
	work_arr = np.sort(work_arr) # sorting is done.
	size_arr = len(work_arr)
	low_size = int(size_arr * low_cut)
	high_size = int(size_arr * high_cut)
	
	z1 = work_arr[low_size]
	z2 = work_arr[size_arr - 1 - high_size]

	return (z1, z2)

def sky_median_sig_clip(input_arr, sig_fract, percent_fract, max_iter=100, low_cut=True, high_cut=True):
	"""Estimating a sky value for a given number of iterations

	@type input_arr: numpy array
	@param input_arr: image data array
	@type sig_fract: float
	@param sig_fract: fraction of sigma clipping
	@type percent_fract: float
	@param percent_fract: convergence fraction
	@type max_iter: integer
	@param max_iter: max. of iterations
	@type low_cut: boolean
	@param low_cut: cut out only low values
	@type high_cut: boolean
	@param high_cut: cut out only high values
	@rtype: tuple
	@return: (sky value, number of iterations)

	"""
	
	work_arr = np.ravel(input_arr)
	old_sky = np.median(work_arr)
	oldStaDesviation = work_arr.std()
	upper_limit = old_sky + sig_fract * oldStaDesviation
	lower_limit = old_sky - sig_fract * oldStaDesviation
	if low_cut and high_cut:
		indices = np.where((work_arr < upper_limit) & (work_arr > lower_limit))
	else:
		if low_cut:
			indices = np.where((work_arr > lower_limit))
		else:
			indices = np.where((work_arr < upper_limit))
	work_arr = work_arr[indices]
	new_sky = np.median(work_arr)
	iteration = 0
	while ((math.fabs(old_sky - new_sky)/new_sky) > percent_fract) and (iteration < max_iter) :
		iteration += 1
		old_sky = new_sky
		oldStaDesviation = work_arr.std()
		upper_limit = old_sky + sig_fract * oldStaDesviation
		lower_limit = old_sky - sig_fract * oldStaDesviation
		if low_cut and high_cut:
			indices = np.where((work_arr < upper_limit) & (work_arr > lower_limit))
		else:
			if low_cut:
				indices = np.where((work_arr > lower_limit))
			else:
				indices = np.where((work_arr < upper_limit))
		work_arr = work_arr[indices]
		new_sky = np.median(work_arr)
	return (new_sky, iteration)

	
def sky_mean_sig_clip(input_arr, sig_fract, percent_fract, max_iter=100, low_cut=True, high_cut=True):
	print "[cvSpace]::sky_mean_sig_clip"
	work_arr = np.ravel(input_arr)
	old_sky = np.mean(work_arr)
	oldStaDesviation = work_arr.std()
	upper_limit = old_sky + sig_fract * oldStaDesviation
	lower_limit = old_sky - sig_fract * oldStaDesviation
	if low_cut and high_cut:
		indices = np.where((work_arr < upper_limit) & (work_arr > lower_limit))
	else:
		if low_cut:
			indices = np.where((work_arr > lower_limit))
		else:
			indices = np.where((work_arr < upper_limit))
	work_arr = work_arr[indices]
	new_sky = np.mean(work_arr)
	iteration = 0
	while ((math.fabs(old_sky - new_sky)/new_sky) > percent_fract) and (iteration < max_iter) :
		iteration += 1
		old_sky = new_sky
		oldStaDesviation = work_arr.std()
		upper_limit = old_sky + sig_fract * oldStaDesviation
		lower_limit = old_sky - sig_fract * oldStaDesviation
		if low_cut and high_cut:
			indices = np.where((work_arr < upper_limit) & (work_arr > lower_limit))
		else:
			if low_cut:
				indices = np.where((work_arr > lower_limit))
			else:
				indices = np.where((work_arr < upper_limit))
		work_arr = work_arr[indices]
		new_sky = np.mean(work_arr)
	return (new_sky, iteration)	
	
def erode(img, kernelSize=5):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		erosion = cv2.erode(img,kernel,iterations = 1)
		return erosion

def dilate(img, kernelSize=5):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		dilateResult = cv2.dilate(img,kernel,iterations = 1)
		return dilateResult


def closeContour(img, kernelSize=5):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		closeResult = cv2.morphologyEx(img,cv2.MORPH_OPEN, kernel)
		return closeResult


def openContour(img, kernelSize=5):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		closeResult = cv2.morphologyEx(img,cv2.MORPH_CLOSE, kernel)
		return closeResult


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
	peakThreshold = (np.mean(flux)-np.amin(flux))/np.e
	maxPeakThreshold = 0
	boxSize = (np.median(size))*np.pi
	print "Median (mediana) box size "+str(boxSize)
	index=0
	lCandidatos = np.zeros(0)
	height, width = img.shape
	blank_image = np.zeros((height, width, 1), np.uint8)
	for k in keyPoints:
		if (img.item(int(k.pt[1]), int(k.pt[0]))>maxPeakThreshold):
			maxPeakThreshold = img.item(int(k.pt[1]), int(k.pt[0]))
		if img.item(int(k.pt[1]), int(k.pt[0]))>=peakThreshold:
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
	maxPeakThreshold = maxPeakThreshold - peakThreshold/5
	return maxPeakThreshold, lCandidatos, blank_image
	
if __name__ == "__main__":
	'''
	img = cv2.imread('tests/hubble-galaxy_1743872i.jpg',0)
	#medianize(img,10,10)
	img2 = segment(img,60,170)
	cv2.imshow('image',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	'''
	fits = fits.open("tests/frame-g-004264-4-0259.fits")
	img = fits[0].data
	img = preEqualizaFits(img)
	
	cv2.imshow('image',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()