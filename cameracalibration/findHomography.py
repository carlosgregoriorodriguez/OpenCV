import cv2;
import numpy as np;
import sys;

if __name__ == "__main__":
	video = True;
	filename = None;
	soften = True;
	original = None;
	img = None;
	rectSize = 30;
	rectangle = True;
	videoSource = 0;
	
	print """
    Runtime keys:
        Q,ESC - quit the program
    
    This program calculates the homography of current images to make it
    match one saved int smallchessboard.jpg""";
			
	
	if (len(sys.argv)>1):
		if (len(sys.argv[1])  == 1):
			video = True;
			videoSource = int(sys.argv[1]);
		else:
			video = False;
			filename = sys.argv[1];
			
	if video:
		cam = cv2.VideoCapture(videoSource);
		cam.set(3, 800);
		cam.set(4, 600);
	else:
		img = cv2.imread(filename);	
		original = np.copy(img);
		
	cv2.namedWindow("main");
	
	firstimg = cv2.imread('../../img/smallchessboard.jpg');
	patternSize = (9,6);
	
	firstimggs = cv2.cvtColor(firstimg, cv2.cv.CV_RGB2GRAY);
		
	patternWasFound0, corners0 = cv2.findChessboardCorners(firstimggs, patternSize);
	
	
	if patternWasFound0:
		criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
		cv2.cornerSubPix(firstimggs, corners0, (5, 5), (-1, -1), criteria);
	else:
		print "Error: pattern was not found on first image";
		
	cv2.drawChessboardCorners(firstimg, patternSize, corners0, patternWasFound0);
	warp = np.zeros(firstimg.shape);
	key = -1;
	while True and patternWasFound0:				
		if (video):
			f,img = cam.read();
		else:
			img = np.copy(original);
		corners = None;
		imggs = cv2.cvtColor(img, cv2.cv.CV_RGB2GRAY);
		patternWasFound, corners = cv2.findChessboardCorners(imggs, patternSize, corners, cv2.CALIB_CB_FAST_CHECK);
		
		if patternWasFound:
			criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
			cv2.cornerSubPix(imggs, corners, (5, 5), (-1, -1), criteria);
		cv2.drawChessboardCorners(img, patternSize, corners, patternWasFound);
		if (patternWasFound):
			homography, mask = cv2.findHomography(corners, corners0, method = cv2.LMEDS)
			print homography
			print "";
			warp = cv2.warpPerspective(img, homography, (640, 480));
			
		else:
			print patternWasFound;
			
		
		cv2.imshow("main",img);
		cv2.imshow("warp",warp);
		cv2.imshow("first",firstimg);
		
		key = cv2.waitKey(5);	
		key = -1 if key == -1 else key & 255;
		if (key == 27 or key == 113):
			break;
