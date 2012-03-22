import cv2;
import numpy as np;
import sys;

def dummy(val):
	pass;

if __name__ == "__main__":
	video = True;
	filename = None;
	soften = True;
	original = None;
	img = None;
	rectSize = 30;
	rectangle = True;
	videoSource = 0;
	
	print """Backprojection test.
    Usage:
        backprojection.py N
            For streaming from /dev/videoN (if overrided, 0 supposed)
        backprojection.py filename
            For still image filename (not recommended for this example)

    Runtime keys:
        S	-	toggle blur input image (reduce noise on hue channel)
        H 	-	take an histogram
        Q,ESC - quit the program""";
			
	
	if (len(sys.argv)>1):
		if (len(sys.argv[1])  == 1):
			video = True;
			videoSource = int(sys.argv[1]);
		else:
			video = False;
			filename = sys.argv[1];
			
	if video:
		cam = cv2.VideoCapture(videoSource);
		cam.set(3, 640);
		cam.set(4, 480);
	else:
		img = cv2.imread(filename);	
		original = np.copy(img);
		
	cv2.namedWindow('backprojection');
	cv2.namedWindow('config');
	
		
	cv2.createTrackbar('rectSize', 'config',25,100, dummy);
	cv2.createTrackbar('histogram threshold', 'config',120,255, dummy);
	
	
	
	key = -1;
	firstHistogram = True;
	while True:				
		if (video):
			f,img = cam.read();
			# Soften the image because the webcam is very bad
			if (soften):
				img = cv2.blur(img, (3,3));
			if (key == 115):
				soften = not soften;
				print "Soften: "+str(soften);
		else:
			img = np.copy(original);
		
		
		histogramThreshold = cv2.getTrackbarPos("histogram threshold","config");
		rectSize = cv2.getTrackbarPos("rectSize","config");
			
		centerX = img.shape[1]/2;
		centerY = img.shape[0]/2;	
		
		imgH,imgS,imgV = cv2.split(cv2.cvtColor( img , cv2.cv.CV_RGB2HSV));


		if (firstHistogram or key == 104):
			firstHistogram = False;
			histItem = cv2.calcHist([imgH[centerY-rectSize:centerY+rectSize,centerX-rectSize:centerX+rectSize]],[0],None,[256],[0,255]);
			histItemOld = histItem.copy();
			print "Took histogram";
		
		
		retval,histItemThresh = cv2.threshold(histItem, max(histItem)*histogramThreshold/255, max(histItem), cv2.THRESH_TOZERO);
		
		if False:
			# Draw the hue histogram on the original image
			img = np.flipud(img);
			histCurrent = cv2.calcHist([imgH],[0],None,[256],[0,255]);
			cv2.normalize(histCurrent ,histCurrent ,0,255,cv2.NORM_MINMAX);
			histCurrentNormalized=np.int32(np.around(histCurrent));
			currentHistogramPoints = np.column_stack((np.arange(256).reshape(256,1),histCurrentNormalized));
			cv2.polylines(img,np.array([currentHistogramPoints],np.int32),False,(255,255,255),1);	
			img = np.flipud(img);
			
		bp = cv2.calcBackProject([imgH], [0], histItemThresh, [0,255], 1);
		thresh_ret,bp_thresh = cv2.threshold(bp,120, 255,cv2.THRESH_BINARY);
		
		# Draw rectangle for object fitting
		if rectangle:
			cv2.rectangle(img, 
						(centerX-rectSize,centerY-rectSize),
						(centerX+rectSize,centerY+rectSize), 
						(255,255,255));
		
		cv2.imshow("backprojection",bp);
		cv2.imshow("backprojection threshold",bp_thresh);
		cv2.imshow("original",img);
		
		key = cv2.waitKey(5);
		if (key == 114):
			rectangle = not rectangle;
			
		if (key == 27 or key == 113):
			break;
