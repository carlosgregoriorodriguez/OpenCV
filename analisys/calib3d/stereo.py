import cv2;
import numpy as np;
import sys;
from optparse import OptionParser



def dummy(val):
	pass;


def printMatrix(matrix, format = '%13.10f', returnString = False):
	s = '';
	for i in range(len(matrix)):
		if (i==0):
			s+='/';
		elif (i==len(matrix)-1):
			s+='\\';
		else:
			s+='|';
		for j in range(len(matrix[i])):
			if (j>0):
				s+=" ";
			s+=format % matrix[i][j];
		if (i==0):
			s+=' \\\n';
		elif (i==len(matrix)-1):
			s+=' /\n';
		else:
			s+=' |\n';
	if returnString:
		return s;
	else:
		print s;
		

def printVector(vector, format = '%13.10f', returnString = False):
	s = '[';
	for i in range(len(vector)):
		if (i>0):
			s+=' ';
		s+=format % vector[i];
	s+=']';
	if returnString:
		return s;
	else:
		print s;

def parseRotationMatrix(R):	
	v = None;
	eigenvalues,eigenvectors = np.linalg.eig(R);
	for i,e in enumerate(eigenvalues):					
		if np.imag(e)==0:
			v = np.real(eigenvectors[:,i]);
			if ((np.imag(eigenvectors[:,i])!=0).any()):
				print v;
				raise BaseException;
	if (v == None):
		print "Eigenvalues:",eigenvalues;
		raise BaseException;
	theta = np.arccos((np.trace(R)-1)/2);
	return theta, v;

def eulerAnglesFromMatrix(R):
	if (abs(R[2][0])!=1):
		theta1 = np.arcsin(R[2][0]);
		psi1 = np.arctan2(R[2][1]/np.cos(theta1),R[2][2]/np.cos(theta1));
		phi1 = np.arctan2(R[1][0]/np.cos(theta1),R[0][0]/np.cos(theta1));
		return [theta1,psi1,phi1];
	else:
		raise BaseException("Not equal to 1");

def findCorners(img):
	corners = None;
	imggs = cv2.cvtColor(img, cv2.cv.CV_RGB2GRAY);
	patternWasFound, corners = cv2.findChessboardCorners(imggs, patternSize, corners, cv2.CALIB_CB_FAST_CHECK);
	# print patternWasFound, corners;
	
	if patternWasFound:
		criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 );
		cv2.cornerSubPix(imggs, corners, (5, 5), (-1, -1), criteria);
	return [patternWasFound,corners];

if __name__ == "__main__":
	
	
	parser = OptionParser();
	parser.add_option("--onecamera", action="store_true",dest="oneCamera",help="Use only one camera");
	(options, args) = parser.parse_args();
	
	img1 = None;
	img1original = None;
	img2 = None;
			
	
	cam1 = cv2.VideoCapture(0);
	cam1.set(3, 640);
	cam1.set(4, 480);
	cam2 = None;
	
	if (not options.oneCamera):
		cam2 = cv2.VideoCapture(1);
		cam2.set(3,640);
		cam2.set(4,480);
		cv2.namedWindow("cam2");
	
	cv2.namedWindow("cam1");
	
	
	squareSize = 2.5;
	
	patternSize = (9, 6);
	patternPoints = np.zeros( (np.prod(patternSize), 3), np.float32 );
	patternPoints[:,:2] = np.indices(patternSize).T.reshape(-1, 2);
	patternPoints *= squareSize;
	
	savedCorners1 = [];
	savedCorners2 = [];
	objectPoints = [];
	
	key = -1;
	firstShot = False;
	
	
	
	
	
	while True:				
		if (options.oneCamera):
			if firstShot:
				img1 = cv2.flip(img1original.copy(),1);
			img2 = cv2.flip(cam1.read()[1],1);
		else:
			img1 = cv2.flip(cam1.read()[1],1);
			img2 = cv2.flip(cam2.read()[1],1);
			
		
		if (not firstShot and options.oneCamera):
			cv2.imshow("cam1",img2);
			patternWasFound, corners = findCorners(img2);
			if (key != 32):
				print "Press spacebar to take the first shot";
			elif (patternWasFound):
				firstShot = True;
				img1original = img2.copy();
			else:
				print "Pattern was not found";        
		else:
			patternWasFound1, corners1 = findCorners(img1);
			patternWasFound2, corners2 = findCorners(img2);
			cv2.drawChessboardCorners(img1, patternSize, corners1, patternWasFound1);
			cv2.drawChessboardCorners(img2, patternSize, corners2, patternWasFound2);
			for corners1a,corners2a in zip(savedCorners1,savedCorners2):				
				cv2.drawChessboardCorners(img1, patternSize, corners1a, True);
				cv2.drawChessboardCorners(img2, patternSize, corners2a, True);
			cv2.imshow("cam1",img1);
			cv2.imshow("cam2",img2);
			
			if (patternWasFound1 and patternWasFound2):
				if (key == 115 and not options.oneCamera):
					savedCorners1 += [corners1];
					savedCorners2 += [corners2];
					objectPoints += [patternPoints];
				elif (key == 115 and options.oneCamera):
					raise BaseException("Option S is only available with two cameras");
				
				h, w = img1.shape[:2]
				cameraMatrix1 = None;
				cameraMatrix2 = None;
				distCoeffs1 = None;
				distCoeffs2 = None;
				R,T,E,F = [None,None,None,None]
				if (len(savedCorners1)>0):
					try:
						ret,cameraMatrix1,distCoeffs1,cameraMatrix2,distCoeffs2,R,T,E,F = cv2.stereoCalibrate(objectPoints, savedCorners1, savedCorners2, (w,h), cameraMatrix1, distCoeffs1,cameraMatrix2,distCoeffs2, R,T,E,F);
					except:
						print len(savedCorners1);
						print len(savedCorners2);
						print savedCorners1;
						print savedCorners2;
				else:	
					ret,cameraMatrix1,distCoeffs1,cameraMatrix2,distCoeffs2,R,T,E,F = cv2.stereoCalibrate([patternPoints], [corners1], [corners2], (w,h), cameraMatrix1, distCoeffs1,cameraMatrix2,distCoeffs2, R,T,E,F);
				print "------------------------"
				printMatrix(R);
				r = cv2.Rodrigues(R)[0];
				
				try:
					theta, vector = parseRotationMatrix(R);
					print "Theta:      %10.7f (%d)" % (theta, theta*360/(2*np.pi));
					print "Vector:     "+printVector(vector,returnString=True);
				except:
					raise
					print "No eigenvalue 1.0";
					
				
				print "Euler:      "+printVector(eulerAnglesFromMatrix(R),returnString=True);
				print "Rodrigues:  "+printVector(r,returnString=True);
				print "Traslation: "+printVector(T,returnString=True);
				
			else:
				pass; # No pattern
		
		key = cv2.waitKey(5);
		key = -1 if key == -1 else 255 & key;
		if (key > 0):
			print key;
		if (key == 27 or key == 113 or key == 1048689 or key == 1048603):
			break;
