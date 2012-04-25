import cv2;
import numpy as np;
import sys;
import time;

if __name__ == "__main__":
	squareSize = 2.8;
	videoSource = 0;
	
	cam = cv2.VideoCapture(videoSource);
	cam.set(3, 800);
	cam.set(4, 600);
	
	patternSize = (9, 6)
	patternPoints = np.zeros( (np.prod(patternSize), 3), np.float32 )
	patternPoints[:,:2] = np.indices(patternSize).T.reshape(-1, 2)
	patternPoints *= squareSize
	
	cv2.namedWindow("main");
	
	objPoints = []
	imgPoints = []
	h, w = 0, 0
	corners = None;
	
	while True:
		f, img = cam.read();
		h,w = img.shape[:2];
		while True:
			# Esta ventana no se abre
			print "esta ventana:"
			cv2.imshow("main",img);
			print "no se abre";
