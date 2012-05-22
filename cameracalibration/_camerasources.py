import cv2;
import numpy as np;

KEY_SPACE = 32;
KEY_B = 98;
KEY_Q = 113;
KEY_ESC = 27;

class CameraSource:
	def __init__(self,src,resolution=(800,600)):
		self.src = src;
		self.cam = cv2.VideoCapture(src);
		self.w,self.h = resolution;
		self.setResolution(self.w,self.h);
		self.calibrated = False;
	
	def setResolution(self,w,h):
		self.cam.set(3,w);
		self.cam.set(4,h);
	
	def calibrate(self, patternPoints, captures = 10):
		objPoints = []
		imgPoints = []
		corners = None;
		frameSkip = 0;
		cameraCalibrationData = None;
		print "Calibration of camera %d" % self.src;
		print "Press SPACE to capture a pattern";
		print "You can stop capturing patterns by pressing B or it will be automatically stopped at %d captures" % captures;
		
		while (len(imgPoints) < captures):
			img = cv2.flip(self.cam.read()[1], 1);
				
			imggs = cv2.cvtColor(img, cv2.cv.CV_RGB2GRAY);
			patternWasFound, corners = cv2.findChessboardCorners(imggs, patternSize, corners, cv2.CALIB_CB_FAST_CHECK);
		
			if patternWasFound:
				criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
				cv2.cornerSubPix(imggs, corners, (5, 5), (-1, -1), criteria);
			cv2.drawChessboardCorners(img, patternSize, corners, patternWasFound);

			cv2.imshow("Camera %d caliration" % self.src,img);

			key = cv2.waitKey(25);
			key = -1 if key == -1 else key & 255;
			if (patternWasFound and key == KEY_SPACE):
				print "Taking a shot... (%d)" % (len(imgPoints)+1);
				imgPoints.append(corners.reshape(-1, 2))
				objPoints.append(patternPoints)
			elif (len(imgPoints) > 0 and key == KEY_B):
				print "Stopping pattern captures";
				break;
			elif (key == KEY_Q or key == KEY_ESC):
				print "Quiting...";
				exit();
				
		# Camera intrinsec
		cameraMatrix = None;
		distCoefs = None;
		self.calibrationData = cv2.calibrateCamera(objPoints+[patternPoints], imgPoints+[corners], (self.w, self.h), cameraMatrix, distCoefs);
#		self.rms, self.cameraMatrix, self.distCoefs, self.rvecs, self.tvecs = self.calibrationData
		# Set this camera as calibrated;
		self.calibrated = True;
				
	def setCalibrationFile(self,filename,patternPoints):
		try:
			f = open(filename, 'r');
			self.calibrationData = pickle.load(f);
			self.calibrated = True;
			f.close();
		except:
			print;
			print "Problem opening %s,let's calibrate it" % filename;
			self.calibrate(patternPoints);
			f = open(filename,'w');
			pickle.dump(self.calibrationData,f);
			f.close();
			print "Camera %d calibrated and data saved to %s" % (self.src,filename);
	
	def getCalibrationData(self):
		if not self.calibrated:
			raise BaseException("Camera was not calibrated yet");	
		return self.calibrationData;
		
	def read(self):
		return cv2.flip(self.cam.read()[1],1);
		
class VirtualCameraSource:
	def __init__(self,realCamera):
		self.realCamera = realCamera;
		self.captureNewFrame();
		self.calibrated = False;
		
	def captureNewFrame(self):
		cv2.namedWindow("Virtual camera capture");
		print "Press SPACE to take a capture as the image for the virtual camera";
		while True:
			img = self.realCamera.read();
			cv2.imshow("Virtual camera capture", img);
			key = cv2.waitKey(25);
			key = -1 if key == -1 else key & 255;
			if (key == KEY_SPACE):
				self.image = img;
				print "Capture taken for the virtual camera";
				break;
			elif (key == KEY_ESC or key == KEY_Q):
				print "Quiting...";
				exit();
				
		cv2.destroyWindow("Virtual camera capture");
	
	def calibrate(self,patternPoints,captures):
		if not self.realCamera.calibrated:
			self.realCamera.calibrate(patternPoints, captures);
		self.calibrationData = self.realCamera.getCalibrationData();
	
	def setCalibrationFile(self,filename,patternPoints):
		raise BaseException("This is a virtual camera, you can't load calibration data for it");
	
	def getCalibrationData(self):
		if not self.calibrated:
			raise BaseException("Camera was not calibrated yet");	
		return self.calibrationData;	
	
	def setResolution(self,w,h):
		pass;
	
	def read(self):
		return self.image;
