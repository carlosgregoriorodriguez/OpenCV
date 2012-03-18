import cv2
import numpy as np
import sys


def dummy(num):
   print "Value: "+str(num)

def getChannel(img, channel):
	if (channel == 0):
		return cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY);
	elif (channel == 1):
		b,g,r = cv2.split(img);
		return r;
	elif (channel == 2):
		b,g,r = cv2.split(img);
		return g;
	elif (channel == 3):
		b,g,r = cv2.split(img);
		return b;
	elif (channel == 4):
		imgHSV =  cv2.cvtColor(img,cv2.cv.CV_RGB2HSV);
		h,s,v = cv2.split(imgHSV);
		return h;
	elif (channel == 5):
		imgHSV =  cv2.cvtColor(img,cv2.cv.CV_RGB2HSV);
		h,s,v = cv2.split(imgHSV);
		return s;
	elif (channel == 6):
		imgHSV =  cv2.cvtColor(img,cv2.cv.CV_RGB2HSV);
		h,s,v = cv2.split(imgHSV);
		return v;

def channelName(num):
	if (num == 0):
		print "Channel: Greyscale";
	elif (num == 1):
		print "Channel: Red";
	elif (num == 2):
		print "Channel: Green";
	elif (num == 3):
		print "Channel: Blue";
	elif (num == 4):
		print "Channel: Hue";
	elif (num == 5):
		print "Channel: Saturation";
	elif (num == 6):
		print "Channel: Value";

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
	cv2.namedWindow('config', cv2.cv.CV_WINDOW_NORMAL);
	"""
	cv2.createTrackbar('number', 'cornerswindow',1,50, dummy);
	cv2.createTrackbar('distance', 'cornerswindow',1,300, dummy);
	cv2.createTrackbar('quality/100', 'cornerswindow',1,150, dummy);
	cv2.createTrackbar('channel', 'cornerswindow',1,6, channelName);
	cv2.createTrackbar('draw on original', 'cornerswindow',1,1, dummy);
	"""
	cv2.createTrackbar("canny tresh1", 'config',600,600, dummy);
	cv2.createTrackbar("canny tresh2", 'config',300,600, dummy);
	cv2.createTrackbar('channel', 'config',0,6, channelName);
	cv2.createTrackbar('draw on original', 'config',0,1, dummy);
	
	while True:		
		if (video):
			f,img = cam.read();
		# Copy of the original image
		imgToDraw = None;
		imgChannel = getChannel(img, cv2.getTrackbarPos("channel","config"));
		canny = cv2.Canny(imgChannel, cv2.getTrackbarPos("canny tresh1","config"), cv2.getTrackbarPos("canny tresh2","config"))
		tmpcontours,hierarchy = cv2.findContours(canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);
		#print contours;
		
		contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in tmpcontours]
		print len(contours)
		#print contours;
		
		if(cv2.getTrackbarPos("draw on original","config") == 1):
			imgToShow = img.copy();
		else:
			imgToShow = canny.copy();
			
		cv2.drawContours(imgToShow, contours, -1, (255,0,0));
			
		cv2.imshow('contours', imgToShow);
		cv2.imshow('canny', canny);
		
		key = cv2.waitKey(5);
		if (key != -1):
			break;
