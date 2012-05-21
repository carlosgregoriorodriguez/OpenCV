import cv2;
import numpy as np;
import sys;

if __name__ == "__main__":
	print """
This program just calibrates the camera and returns the camera matrix, and rvecs&tvecs
It's just a basic example

Press ESC or Q to exit.""";
	squareSize = 2.8;
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

		
		h, w = img.shape[:2]
		
		if patternWasFound:
			camera_matrix = None;
			dist_coefs = None;
			rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(objPoints+[patternPoints], imgPoints+[corners], (w, h), camera_matrix, dist_coefs)
			print "RMS:", rms
			print "camera matrix:\n", camera_matrix
			print "distortion coefficients: ", dist_coefs.ravel()
			print "rvecs: ",rvecs[-1]
			print "tvecs: ",tvecs[-1]
		
		key = cv2.waitKey(5);
		key = -1 if key == -1 else key & 255;
		if (key == 27 or key == 113):
			print "Quiting...";
			break;
