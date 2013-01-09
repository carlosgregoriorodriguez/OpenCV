import cv2
import numpy as np
import sys
import time

def channel2eq(num):
   print "Channel to equalize: "+str(num)
def channel2show(num):
   print "Channel to show: "+str(num)

def modeName(num):
	if (num == 0):
		print "Color mode: BGR";
	elif (num == 1):
		print "Color mode: HSV";
	elif (num == 2):
		print "Color mode: HLS";

def help():
   print ">"*40
   print "Usage:"
   print "python equalizahist_channels [camera number|file name]"
   print "If no argument open the file ../../img/stop.jpg"
   print "color mode: 0 BGR; 1 HSV; 2 HLS"
   print "channel to equalize: 0 all channels ; 1,2,3 first to third; 4 none"
   print "channel to show: 0 all channels ; 1,2,3 first to third"
   print "p to file equalized img"
   print "<"*40
if __name__ == "__main__":
        help()
	video = False;
	filename = '../../img/stop.jpg';
	cam = False;
	img = None;
	if (len(sys.argv)>1):
           try:
              x = int(sys.argv[1])
              cam = cv2.VideoCapture(int(sys.argv[1]));
              cam.set(3, 640);
              cam.set(4, 480);
              video = True;
           except ValueError:
              filename = sys.argv[1];

	
	original = None;
	cv2.namedWindow('image equalized');
	cv2.namedWindow('original');
        cv2.namedWindow('image in color mode')
	cv2.namedWindow('configwindow', cv2.cv.CV_WINDOW_NORMAL);
	cv2.createTrackbar('color mode', 'configwindow',0,2, modeName);
	cv2.createTrackbar('channel to equalize', 'configwindow',0,4, channel2eq);
	cv2.createTrackbar('channel to show', 'configwindow',0,3, channel2show);
	
		
	while True:		
		if (video):
			f,img = cam.read();
		else:
                   img = cv2.imread(filename);

		ch3, ch2, ch1 = None,None,None;
		imgToShow = None;
		
		mode = cv2.getTrackbarPos("color mode","configwindow");
		equalizeChannel = cv2.getTrackbarPos("channel to equalize","configwindow");
		showChannel = cv2.getTrackbarPos("channel to show","configwindow");
		
		
		if (mode == 0):
			ch1,ch2,ch3 = cv2.split(img);
                        imgMode = img
		elif(mode == 1):
                        imgMode = cv2.cvtColor(img,cv2.cv.CV_BGR2HSV)
			ch1,ch2,ch3 = cv2.split(imgMode)
		else:
                        imgMode =  cv2.cvtColor(img,cv2.cv.CV_BGR2HLS)
			ch1,ch2,ch3 = cv2.split(imgMode);
		
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
                           imgToShow = cv2.merge([ch1,ch2,ch3])
                           imgToBGR = imgToShow
			elif(mode == 1):
                           imgToShow = cv2.merge([ch1,ch2,ch3])
                           imgToBGR = cv2.cvtColor(imgToShow,cv2.cv.CV_HSV2BGR);
			else:
                           imgToShow = cv2.merge([ch1,ch2,ch3])
                           imgToBGR = cv2.cvtColor(imgToShow,cv2.cv.CV_HLS2BGR);
	
		elif (showChannel == 1):
			imgToShow = ch1;
		elif (showChannel == 2):
			imgToShow = ch2;
		elif (showChannel == 3):
			imgToShow = ch3;
		
		cv2.imshow('image equalized', imgToShow);
                cv2.imshow('image in color mode',imgMode)
		cv2.imshow('original', img);
		cv2.imshow('equalized to BGR', imgToBGR)
		key = cv2.waitKey(5);
		if (key != -1):
                   if key == 112 : #tecla p 
                      outimg = "output_"+str(int(time.time()))+".jpeg"
                      print "output image:", outimg
                      cv2.imwrite(outimg, imgToShow)
                   if key & 255 == 113 : #tecla q
                       break
