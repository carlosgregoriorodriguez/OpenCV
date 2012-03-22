import cv2
import numpy as np
import sys


def dummy(num):
   print "Value: "+str(num)


if __name__ == "__main__":
	video = False;
	filename = '../img/stop.jpg';
	cam = False;
	
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
	original = None;
	cv2.namedWindow('cornerswindow');
	cv2.createTrackbar('number', 'cornerswindow',1,50, dummy);
	cv2.createTrackbar('distance', 'cornerswindow',1,300, dummy);
	cv2.createTrackbar('quality/100', 'cornerswindow',1,150, dummy);
	
	
	print "here";	
	while True:		
		if (video):
			f,img = cam.read();
		# Copy of the original image
		copy = img.copy();
		imgGreyscale = cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY);
		corners = cv2.goodFeaturesToTrack(imgGreyscale, cv2.getTrackbarPos("number","cornerswindow"), float(cv2.getTrackbarPos("quality/100","cornerswindow")+1)/100, cv2.getTrackbarPos("distance","cornerswindow"));
		if (corners != None):
			for corner in corners:
				cv2.ellipse(copy, (corner[0][0], corner[0][1]),  (10,10), 0, 0, 360, 255, -1 );
		
		cv2.imshow('cornerswindow', copy);
		
		key = cv2.waitKey(5);
		if (key != -1):
			break;
