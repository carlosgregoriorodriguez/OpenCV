import cv2
import numpy as np
import sys


def dummy(num):
   print "Value: "+str(num)


def modeName(num):
	if (num == 0):
		print "Color mode: RGB";
	elif (num == 1):
		print "Color mode: HSV";
	elif (num == 2):
		print "Color mode: HLS";

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
	cv2.namedWindow('imagewindow');
	cv2.namedWindow('original');
	cv2.namedWindow('configwindow', cv2.cv.CV_WINDOW_NORMAL);
	cv2.createTrackbar('color mode', 'configwindow',1,2, modeName);
	cv2.createTrackbar('channel to equalize', 'configwindow',2,3, dummy);
	cv2.createTrackbar('channel to show', 'configwindow',0,3, dummy);
	
		
	while True:		
		if (video):
			f,img = cam.read();
		# Copy of the original image
		
		ch3, ch2, ch1 = None,None,None;
		imgToShow = None;
		
		mode = cv2.getTrackbarPos("color mode","configwindow");
		equalizeChannel = cv2.getTrackbarPos("channel to equalize","configwindow");
		showChannel = cv2.getTrackbarPos("channel to show","configwindow");
		
		
		if (mode == 0):
			ch3,ch2,ch1 = cv2.split(img);
		elif(mode == 1):
			ch1,ch2,ch3 = cv2.split(cv2.cvtColor(img,cv2.cv.CV_RGB2HSV));
		else:
			ch1,ch2,ch3 = cv2.split(cv2.cvtColor(img,cv2.cv.CV_RGB2HLS));
		
		if(equalizeChannel == 0):
			ch1 = cv2.equalizeHist(ch1);
			ch2 = cv2.equalizeHist(ch2);
			ch3 = cv2.equalizeHist(ch3);
		elif(equalizeChannel == 1):
			ch1 = cv2.equalizeHist(ch1);
		elif(equalizeChannel == 2):
			ch2 = cv2.equalizeHist(ch2);
		elif(equalizeChannel == 3):
			ch3 = cv2.equalizeHist(ch3);
		
		if (showChannel == 0):
			if(mode == 0):
				imgToShow = cv2.merge([ch3, ch2, ch1]);
			elif(mode == 1):
				imgToShow = cv2.cvtColor(cv2.merge([ch1,ch2,ch3]),cv2.cv.CV_HSV2RGB);
			else:
				imgToShow = cv2.cvtColor(cv2.merge([ch1,ch2,ch3]),cv2.cv.CV_HLS2RGB);
				
		elif (showChannel == 1):
			imgToShow = ch1;
		elif (showChannel == 2):
			imgToShow = ch2;
		elif (showChannel == 3):
			imgToShow = ch3;
		
		cv2.imshow('imagewindow', imgToShow);
		cv2.imshow('original', img);
		
		key = cv2.waitKey(5);
		if (key != -1):
			break;
