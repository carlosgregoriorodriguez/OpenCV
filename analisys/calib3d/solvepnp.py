import cv2;
import numpy as np;
import sys;

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
	while (len(imgPoints) < 5):
		f, img = cam.read();
				
		imggs = cv2.cvtColor(img, cv2.cv.CV_RGB2GRAY);
		patternWasFound, corners = cv2.findChessboardCorners(imggs, patternSize, corners, cv2.CALIB_CB_FAST_CHECK);
		
		if patternWasFound:
			criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
			cv2.cornerSubPix(imggs, corners, (5, 5), (-1, -1), criteria);
		cv2.drawChessboardCorners(img, patternSize, corners, patternWasFound);

		cv2.imshow("main",img);

		key = cv2.waitKey(5);
		frameSkip -= 1;
		if (patternWasFound and frameSkip < 1):
			print "Taking a shot...(%d)" % len(imgPoints);
			imgPoints.append(corners.reshape(-1, 2))
			objPoints.append(patternPoints)
			frameSkip = 10;
	
	h, w = img.shape[:2]
	# Camera intrinsec
	cameraMatrix = None;
	distCoefs = None;
	rms, cameraMatrix, distCoefs, rvecs, tvecs = cv2.calibrateCamera(objPoints+[patternPoints], imgPoints+[corners], (w, h), cameraMatrix, distCoefs)
	
	while True:
		f, img = cam.read();
		h, w = img.shape[:2]
				
		imggs = cv2.cvtColor(img, cv2.cv.CV_RGB2GRAY);
		patternWasFound, corners = cv2.findChessboardCorners(imggs, patternSize, corners, cv2.CALIB_CB_FAST_CHECK);
		
		if patternWasFound:
			criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
			cv2.cornerSubPix(imggs, corners, (5, 5), (-1, -1), criteria);
		cv2.drawChessboardCorners(img, patternSize, corners, patternWasFound);

		cv2.imshow("main",img);

		
		
		if patternWasFound:
			rvec,tvec = cv2.solvePnP(patternPoints, corners, cameraMatrix, distCoefs);
			print "rvecs: ",rvec
			print "tvecs: ",tvec
		
		key = cv2.waitKey(5);
		if (key == 27 or key == 113):
			print "Quiting...";
			break;
