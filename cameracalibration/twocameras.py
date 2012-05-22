import cv2;
import numpy as np;
import sys;
import pickle;
from _pygameview_solvepnp import *;
from _camerasources import *;
from multiprocessing import Process,Array,Lock
from optparse import OptionParser;


# Command line options parser
def parse_options():
	parser = OptionParser();
	parser.add_option("--onecamera", action="store_true", dest="onecamera", help="Use only one camera");
	parser.add_option("--firstsource", type="int", default=0, dest="firstsource", help="First source of video");
	parser.add_option("--firstcalibration", type="string", dest="firstcalibration", help="Calibration data file for the first source of video. If ommited, new calibration will be performed. If not ommited but the file doesn't exist, new calibration will be performed and the data will be saved into the specified file");
	parser.add_option("--secondsource", type="int", default=1, dest="secondsource", help="Second source of video. Incompatible with --onecamera");
	parser.add_option("--secondcalibration", type="string", dest="secondcalibration", help="Calibration data file for the second source of video. If ommited, new calibration will be performed. If not ommited but the file doesn't exist, new calibration will be performed and the data will be saved into the specified file. Incompatible with --onecamera. For one camera, the second calibration data is the same as for the first camera (obviously)");
	parser.add_option("--resolution", type="int", nargs=2, default=(800,600), dest="resolution", help="Cameras resolution");
	parser.add_option("--pattern", type="int", nargs=2, default=(6,3), dest="patternsize", help="Pattern size (inner corners)");
	parser.add_option("--squaresize", type="float", default=1.0, dest="squaresize", help="Square size");
	return parser.parse_args();

def getCorners(img,patternSize);
	corners = None;
	imggs = cv2.cvtColor(img, cv2.cv.CV_RGB2GRAY);
	patternWasFound, corners = cv2.findChessboardCorners(imggs, patternSize, corners, cv2.CALIB_CB_FAST_CHECK);
	
	if patternWasFound:
		criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
		cv2.cornerSubPix(imggs, corners, (5, 5), (-1, -1), criteria);
	return patternWasFound,corners;



if __name__ == "__main__":
	(options, args) = parse_options();
	
	# Create virtual pattern to calibrate
	squareSize = options.squaresize;
	patternSize = options.patternsize;
	patternPoints = np.zeros( (np.prod(patternSize), 3), np.float32 )
	patternPoints[:,:2] = np.indices(patternSize).T.reshape(-1, 2)
	patternPoints *= squareSize
	
	# Creating first camera
	cam1 = CameraSource(options.firstsource, options.resolution);
	# Calibration of the first camera
	if options.firstcalibration:
		cam1.setCalibrationFile(options.firstcalibration, patternPoints);
	else:
		cam1.calibrate(patternPoints, 10);
		
	# Second camera
	if options.onecamera:
		cam2 = VirtualCameraSource(cam1);
		# Calibration of the virtual camera is just getting the calibration data from the first one
		cam2.calibrate(patternPoints, 10);
	else:
		cam2 = CameraSource(options.secondsource, options.resolution);
		if options.secondcalibration:
			cam2.setCalibrationFile(options.secondcalibration, patternPoints);
		else:
			cam2.calibrate(patternPoints, 10);
	
	rms, cameraMatrix, distCoefs, rvecs, tvecs = cam1.getCalibrationData();
			
	# pygame init
	
	p = None;
	# Pygame init end
	Rarr = Array('d',[0.0]*3);
	Tarr = Array('d',[0.0]*3);
	lock = Lock();
	
	while True:
		img = cam1.read();
		w,h = options.resolution;
		
		patternWasFound,corners = getCorners(img, patternSize);
		
		cv2.drawChessboardCorners(img, patternSize, corners, patternWasFound);
		
		cv2.circle(img,(int(cameraMatrix[0][2]),int(cameraMatrix[1][2])),10,(255,255,0),2)
		cv2.imshow("main",img);

		
		
		if patternWasFound:			
			solved,R,T = cv2.solvePnP(patternPoints, corners, cameraMatrix, distCoefs);
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
		if (key == KEY_ESC or key == KEY_Q):
			print "Quiting...";
			break;
