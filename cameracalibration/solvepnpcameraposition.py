import cv2;
import numpy as np;
import sys;
import pickle;
from _pygameview_solvepnp import *;
from multiprocessing import Process,Array,Lock



if __name__ == "__main__":
	squareSize = 1.0;
	videoSource = 0;
	
	cam = cv2.VideoCapture(videoSource);
	cam.set(3, 800);
	cam.set(4, 600);
	
	patternSize = (9, 6)
	patternPoints = np.zeros( (np.prod(patternSize), 3), np.float32 )
	patternPoints[:,:2] = np.indices(patternSize).T.reshape(-1, 2)
	patternPoints *= squareSize
	
	objPoints = []
	imgPoints = []
	h, w = 0, 0
	corners = None;
	frameSkip = 0;
	cameraCalibrationData = None;
	if (len(sys.argv) > 1 and sys.argv[1] == 'calibrate'):
		while (len(imgPoints) < 10):
			img = cv2.flip(cam.read()[1], 1);
				
			imggs = cv2.cvtColor(img, cv2.cv.CV_RGB2GRAY);
			patternWasFound, corners = cv2.findChessboardCorners(imggs, patternSize, corners, cv2.CALIB_CB_FAST_CHECK);
		
			if patternWasFound:
				criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
				cv2.cornerSubPix(imggs, corners, (5, 5), (-1, -1), criteria);
			cv2.drawChessboardCorners(img, patternSize, corners, patternWasFound);

			cv2.imshow("main",img);

			key = cv2.waitKey(5);
			key = -1 if key == -1 else key & 255;
			if (patternWasFound and key == 32):
				print "Taking a shot...(%d)" % len(imgPoints);
				imgPoints.append(corners.reshape(-1, 2))
				objPoints.append(patternPoints)
	
		h, w = img.shape[:2]
		# Camera intrinsec
		cameraMatrix = None;
		distCoefs = None;
		cameraCalibrationData = cv2.calibrateCamera(objPoints+[patternPoints], imgPoints+[corners], (w, h), cameraMatrix, distCoefs);
		f = open('calib.dat','w');
		pickle.dump(cameraCalibrationData,f);
		f.close();
	else:
		f = open('calib.dat', 'r');
		cameraCalibrationData = pickle.load(f);
		f.close();
		
	rms, cameraMatrix, distCoefs, rvecs, tvecs = cameraCalibrationData
	print cameraMatrix
	
	# pygame init
	
	p = None;
	# Pygame init end
	Rarr = Array('d',[0.0]*3);
	Tarr = Array('d',[0.0]*3);
	lock = Lock();
	
	while True:
		img = cv2.flip(cam.read()[1], 1);
		h, w = img.shape[:2]
				
		imggs = cv2.cvtColor(img, cv2.cv.CV_RGB2GRAY);
		patternWasFound, corners = cv2.findChessboardCorners(imggs, patternSize, corners, cv2.CALIB_CB_FAST_CHECK);
		
		if patternWasFound:
			criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
			cv2.cornerSubPix(imggs, corners, (5, 5), (-1, -1), criteria);
		cv2.drawChessboardCorners(img, patternSize, corners, patternWasFound);
		
		cv2.circle(img,(int(cameraMatrix[0][2]),int(cameraMatrix[1][2])),10,(255,255,0),2)
		cv2.imshow("main",img);

		
		
		if patternWasFound:			
			R,T = cv2.solvePnP(patternPoints, corners, cameraMatrix, distCoefs);
			# print "R:",R
			# print "Rodrigues:",cv2.Rodrigues(R);			
			lock.acquire();
			Rarr[:] = R;
			Tarr[:] = T;
			lock.release();
			if not p:
				p = Process(target=pygameProcess, args=(Rarr,Tarr,lock));
				p.start();
		
		
		
		key = cv2.waitKey(5);
		key = -1 if key == -1 else key & 255;
		if (key != -1):
			print key;
		if (key == 27 or key == 113):
			print "Quiting...";
			break;
