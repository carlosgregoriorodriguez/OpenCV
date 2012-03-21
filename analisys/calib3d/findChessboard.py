import cv2;
import numpy as np;
import sys;

def dummy(val):
	pass;

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
    Usage:
        findChessboard.py N
            For streaming from /dev/videoN (if overrided, 0 supposed)
        findChessboard.py filename
            For still image filename (not recommended for this example)

    Runtime keys:
        Q,ESC - quit the program""";
			
	
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
	
		
	#cv2.createTrackbar('rectSize', 'config',25,100, dummy);
	#cv2.createTrackbar('histogram threshold', 'config',120,255, dummy);
	
	
	
	key = -1;
	firstHistogram = True;
	while True:				
		if (video):
			f,img = cam.read();
		else:
			img = np.copy(original);
		patternSize = (9,6);
		corners = None;
		imggs = cv2.cvtColor(img, cv2.cv.CV_RGB2GRAY);
		patternWasFound, corners = cv2.findChessboardCorners(imggs, patternSize, corners, cv2.CALIB_CB_FAST_CHECK);
		print patternWasFound, corners;
		
		if patternWasFound:
			criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
			cv2.cornerSubPix(imggs, corners, (5, 5), (-1, -1), criteria);
		cv2.drawChessboardCorners(img, patternSize, corners, patternWasFound);
				
		cv2.imshow("main",img);
		
		key = cv2.waitKey(5);	
		if (key == 27 or key == 113 or key == 1048689 or key == 1048603):
			break;
