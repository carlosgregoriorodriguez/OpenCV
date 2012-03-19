import cv2;
import numpy as np;
import sys;



if __name__ == "__main__":
	video = False;
	filename = '../../img/stop.jpg';
	soften = True;
	original = None;
	img = None;
	if (len(sys.argv)>1):
		if (len(sys.argv[1])  == 1):
			video = True;
			cam = cv2.VideoCapture(int(sys.argv[1]));
			cam.set(3, 640);
			cam.set(4, 480);
		else:
			filename = sys.argv[1];
	if (not video):
		img = cv2.imread(filename);	
		original = np.copy(img);
	cv2.namedWindow('backprojection');

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
				
		
		imgH,imgS,imgV = cv2.split(cv2.cvtColor( img , cv2.cv.CV_RGB2HSV));

		# Creating x coordenates
		bins = np.arange(256).reshape(256,1);
		
		# Colors just for drawing histogram lines.
		# Same are used for hsv histograms
		color = [ (255,0,0),(0,255,0),(0,0,255) ];		


		if (firstHistogram or key == 104):
			firstHistogram = False;
			hist_item = cv2.calcHist([imgH],[0],None,[256],[0,255]);
			print "Took histogram";
		
		img = np.flipud(img);
		histCurrent = cv2.calcHist([imgH],[0],None,[256],[0,255]);
		# Normalize histogram from 0 to 255
		cv2.normalize(histCurrent ,histCurrent ,0,255,cv2.NORM_MINMAX);
		# Round and convert to integers
		histCurrentNormalized=np.int32(np.around(histCurrent));
		# Stack the points x coordenates with y values
		currentHistogramPoints = np.column_stack((np.arange(256).reshape(256,1),histCurrentNormalized));
		# Draw the points with their color
		cv2.polylines(img,np.array([currentHistogramPoints],np.int32),False,(255,255,255),1);	
		img = np.flipud(img);
			
		bp = cv2.calcBackProject([imgH], [0], hist_item, [0,255], 1);
		thresh_ret,bp_thresh = cv2.threshold(bp,120, 255,cv2.THRESH_BINARY);
		
		
		cv2.imshow("backprojection",bp);
		cv2.imshow("backprojection threshold",bp_thresh);
		cv2.imshow("hue",imgH);
		cv2.imshow("original",img);
		
		key = cv2.waitKey(5);
		if (key == 27 or key == 113):
			break;
