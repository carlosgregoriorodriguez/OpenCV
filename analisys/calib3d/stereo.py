import cv2;
import numpy as np;
import sys;
from optparse import OptionParser


SCREEN_SIZE = (800, 600)

from math import radians 

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from gameobjects.matrix44 import *
from gameobjects.vector3 import *

def dummy(val):
	pass;


def resize(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60.0, float(width)/height, .1, 1000.)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()


def init():
	glEnable(GL_DEPTH_TEST)
	
	glShadeModel(GL_FLAT)
	glClearColor(1.0, 1.0, 1.0, 0.0)
	
	glEnable(GL_COLOR_MATERIAL)
	
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)        
	glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))  
    
    
class Cube(object):
    
    
	def __init__(self, position, color):
    
		self.position = position
		self.color = color
    
	num_faces = 6

	vertices = [ (0.0, 0.0, 1.0),
				(1.0, 0.0, 1.0),
				(1.0, 1.0, 1.0),
				(0.0, 1.0, 1.0),
				(0.0, 0.0, 0.0),
				(1.0, 0.0, 0.0),
				(1.0, 1.0, 0.0),
				(0.0, 1.0, 0.0) ]

	normals = [ (0.0, 0.0, +1.0),  # front
				(0.0, 0.0, -1.0),  # back
				(+1.0, 0.0, 0.0),  # right
				(-1.0, 0.0, 0.0),  # left 
				(0.0, +1.0, 0.0),  # top
				(0.0, -1.0, 0.0) ] # bottom

	vertex_indices = [ (0, 1, 2, 3),  # front
						(4, 5, 6, 7),  # back
						(1, 5, 6, 2),  # right
						(0, 4, 7, 3),  # left
						(3, 2, 6, 7),  # top
						(0, 1, 5, 4) ] # bottom    

	def render(self):                

		glColor( self.color )

		# Adjust all the vertices so that the cube is at self.position
		vertices = [tuple(Vector3(v) + self.position) for v in self.vertices]

		# Draw all 6 faces of the cube
		glBegin(GL_QUADS)

		for face_no in xrange(self.num_faces):
				    
			glNormal3dv( self.normals[face_no] )

			v1, v2, v3, v4 = self.vertex_indices[face_no]
				
			glVertex( vertices[v1] )
			glVertex( vertices[v2] )
			glVertex( vertices[v3] )
			glVertex( vertices[v4] )            

		glEnd()  
		
class World(object):
    
    def __init__(self):
        
#        map_surface = pygame.image.load("map.png")
#        map_surface.lock()
#        
#        w, h = map_surface.get_size()
#        
#        self.cubes = []
#        
#         Create a cube for every non-white pixel
#        for y in range(h):            
#            for x in range(w):
#                                
#                r, g, b, a = map_surface.get_at((x, y))
#                
#                if (r, g, b) != (255, 255, 255):
#                    
#                    gl_col = (r/255.0, g/255.0, b/255.0)
#                    position = (float(x), 0.0, float(y))
#                    cube = Cube( position, gl_col )
#                    self.cubes.append(cube)                    
#                
#        
#        map_surface.unlock()
    	self.chessboard = Cube((0.0,0.0,0.0),(1.0,0.0,0.0));
        self.display_list = None
    
    def render(self):
                
        if self.display_list is None:
            
            # Create a display list
            self.display_list = glGenLists(1)                
            glNewList(self.display_list, GL_COMPILE)
            
            # Draw the cubes
            self.chessboard.render()
                
            # End the display list
            glEndList()
            
        else:
            
            # Render the display list            
            glCallList(self.display_list)		


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
	
	
	# pygame init
	
	pygame.init()
	screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
	
	resize(*SCREEN_SIZE)
	init()
	
	clock = pygame.time.Clock()    
	
	glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))    
	glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
	
	# This object renders the 'map'
	world = World()        
	
	# Camera transform matrix
	camera_matrix = Matrix44()
	camera_matrix.translate = (10.0, .6, 10.0)
	camera_matrix.translate = (-10.0, -1.0, -1.0)
	
	# Initialize speeds and directions
	rotation_direction = Vector3()
	rotation_speed = radians(90.0)
	movement_direction = Vector3()
	movement_speed = 5.0  
	
	# Pygame init end
	
	
	
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
			
		
		# Pygame
		# Clear screen
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
						
		time_passed = clock.tick()
		time_passed_seconds = time_passed / 1000.
		
		pressed = pygame.key.get_pressed()
		
		# Reset rotation and movement directions
		rotation_direction.set(0.0, 0.0, 0.0)
		movement_direction.set(0.0, 0.0, 0.0)
		# Modify direction vectors for key presses
		if (pressed[K_LEFT] or key == 82):
			rotation_direction.y = +1.0
		elif pressed[K_RIGHT]:
			rotation_direction.y = -1.0
		if (pressed[K_UP] or key == 83):
			rotation_direction.x = -1.0
		elif pressed[K_DOWN]:
			rotation_direction.x = +1.0
		if pressed[K_z]:
			rotation_direction.z = -1.0
		elif pressed[K_x]:
			rotation_direction.z = +1.0            
		if pressed[K_q]:
			movement_direction.z = -1.0
		elif pressed[K_a]:
			movement_direction.z = +1.0
		
		# Calculate rotation matrix and multiply by camera matrix    
		rotation = rotation_direction * rotation_speed * time_passed_seconds
		rotation_matrix = Matrix44.xyz_rotation(*rotation)        
		camera_matrix *= rotation_matrix
		print camera_matrix;
		try:
			camera_matrix.translate = tuple(T);
		except:
			print "no T";
		print camera_matrix;
		print rotation_matrix;
		
		# Calcluate movment and add it to camera matrix translate
		heading = Vector3(camera_matrix.forward)
		movement = heading * movement_direction.z * movement_speed                    
		camera_matrix.translate += movement * time_passed_seconds
		
		# Upload the inverse camera matrix to OpenGL
		glLoadMatrixd(camera_matrix.get_inverse().to_opengl())
				
		# Light must be transformed as well
		glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0)) 
				
		# Render the map
		world.render()
		
				
		# Show the screen
		pygame.display.flip()
