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
	cv2.namedWindow('cornerswindow');
	cv2.createTrackbar('rho', 'cornerswindow',90,100, dummy);
	cv2.createTrackbar('theta', 'cornerswindow',1,10, dummy);
	cv2.createTrackbar('threshold', 'cornerswindow',6000,8000, dummy);
	cv2.createTrackbar('channel', 'cornerswindow',1,6, channelName);
	cv2.createTrackbar('draw on original', 'cornerswindow',1,1, dummy);
	
	while True:		
		if (video):
			f,img = cam.read();
		# Copy of the original image
		imgToDraw = None;
		imgChannel = getChannel(img, cv2.getTrackbarPos("channel","cornerswindow"));
		
		
		if(cv2.getTrackbarPos("draw on original","cornerswindow") == 1):
			imgToShow = img.copy();
		else:
			imgToShow = imgChannel;
		
		rho = (cv2.getTrackbarPos("rho","cornerswindow")+1)/10.0;
		theta = (cv2.getTrackbarPos("theta","cornerswindow")+1)/10.0;
		threshold = cv2.getTrackbarPos("threshold","cornerswindow")+1;
		lines = cv2.HoughLinesP(imgChannel.copy(), rho, theta, threshold);
		print lines;
		print "---";
		try:
			print len(lines[0]);
			for line in lines[0]:
				cv2.line(imgToShow,(line[0],line[1]), (line[2],line[3]),(0,255,0));
		except:
			pass;
		
			
#		if (corners != None):
#			for corner in corners:
#				cv2.circle(imgToShow, (corner[0][0], corner[0][1]),  12, (255,255,255), 2 );
#				cv2.circle(imgToShow, (corner[0][0], corner[0][1]),  14, (0,0,0), 1 );
		
		cv2.imshow('cornerswindow', imgToShow);
		
		key = cv2.waitKey(5);
		if (key != -1):
			break;
