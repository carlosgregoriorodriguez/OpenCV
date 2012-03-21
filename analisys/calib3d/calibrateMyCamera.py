import cv2;
import numpy as np;
import sys;

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
	
	objPoints = []
	imgPoints = []
	h, w = 0, 0
	corners = None;
	
	while True:
		f, img = cam.read();
				
		imggs = cv2.cvtColor(img, cv2.cv.CV_RGB2GRAY);
		patternWasFound, corners = cv2.findChessboardCorners(imggs, patternSize, corners, cv2.CALIB_CB_FAST_CHECK);
		
		if patternWasFound:
			criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
			cv2.cornerSubPix(imggs, corners, (5, 5), (-1, -1), criteria);
		cv2.drawChessboardCorners(img, patternSize, corners, patternWasFound);

		cv2.imshow("main",img);

		key = cv2.waitKey(5);
		
		h, w = img.shape[:2]
        
		if (key == 32): # space
			if not patternWasFound:
				print "No pattern was found";
			else:
				print "Taking a shot...(%d)" % len(imgPoints);
				imgPoints.append(corners.reshape(-1, 2))
				objPoints.append(patternPoints)
				
		elif (key == 115): # S
			print "Calculating...";
			camera_matrix = None;
			dist_coefs = None;
			rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, (w, h), camera_matrix, dist_coefs)
			print "RMS:", rms
			print "camera matrix:\n", camera_matrix
			print "distortion coefficients: ", dist_coefs.ravel()
			print "rvecs: ",rvecs
			print "tvecs: ",tvecs
			
			#print "Rodrigues:\n", cv2.Rodrigues(rvecs[0]);
			
		elif (key == 27 or key == 113):
			print "Quiting...";
			break;
