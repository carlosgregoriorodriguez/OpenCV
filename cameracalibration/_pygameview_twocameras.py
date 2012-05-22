from math import radians 

import numpy as np;

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from linearalgebratools.matrix44 import *
from linearalgebratools.vector3 import *


SCREEN_SIZE = (640,480)


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
    
    
class Chessboard(object):
    
    
	def __init__(self, position, color):
    
		self.position = position
		self.color = color
    
	num_faces = 6

	vertices = [ (-1.0, -1.0, 1.0),
				(1.0, -1.0, 1.0),
				(1.0, 1.0, 1.0),
				(-1.0, 1.0, 1.0),
				(-1.0, -1.0, -1.0),
				(1.0, -1.0, -1.0),
				(1.0, 1.0, -1.0),
				(-1.0, 1.0, -1.0) ]

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
		vertices = [tuple(Vector3(v)) for v in self.vertices]
		# print "rendering cube";
		glPushMatrix();
		glLoadIdentity();
		glScale(5.,5.,1.);
		
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
		glPopMatrix();
		
class Camera():
	def __init__(self, position, color):
    
		self.position = position
		self.color = color

	num_faces = 6

	vertices = [ (-1.0, -1.0, 1.0),
				(1.0, -1.0, 1.0),
				(1.0, 1.0, 1.0),
				(-1.0, 1.0, 1.0),
				(-1.0, -1.0, -1.0),
				(1.0, -1.0, -1.0),
				(1.0, 1.0, -1.0),
				(-1.0, 1.0, -1.0) ]

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
	def render (self):
		glColor(self.color);
		
		# Adjust all the vertices so that the cube is at self.position
		vertices = [tuple(Vector3(v)) for v in self.vertices]
		# print "rendering cube";
		glPushMatrix();
		glLoadIdentity();
		print self.T;
		rNorm = np.sqrt(self.R[0]**2+self.R[1]**2+self.R[2]**2);
		glRotate(rNorm*180/np.pi,self.R[0],-self.R[1],self.R[2]);
		glTranslate(*self.T);
		glScale(5.,5.,5.);
		
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
		glPopMatrix();
		
def pygameProcess(Rarr,Tarr,lock):
	pygame.init()
	screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
	
	resize(*SCREEN_SIZE)
	init()
	
	clock = pygame.time.Clock()    
	
	glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))    
	glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
	
	chessboard = Chessboard((0.0,0.0,400.0),(1.0,0.0,0.0));
	camera1 = Camera((0.,0.,0.),(0.,1.,0.));
	camera2 = Camera((0.,0.,0.),(0.,0.,1.));
	
	# Camera transform matrix
	camera_matrix = Matrix44()
	# camera_matrix.translate = (10.0, .6, 10.0)
	camera_matrix.translate = (0.0, 0.0, -100.0)
	
	
	while True:
		lock.acquire();
		R1 = np.array(list(R1arr));
		T1 = np.array(list(T1arr));
		R2 = np.array(list(R2arr));
		T2 = np.array(list(T2arr));
		lock.release();
		camera1.T = T1*-2;
		camera1.R = R1;
		camera2.T = T2*-2;
		camera2.R = R2;
		
		# print R*180/np.pi;
		
		# Pygame
		# Clear screen
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
					
		# Upload the inverse camera matrix to OpenGL
		glLoadMatrixd(camera_matrix.get_inverse().to_opengl())
			
		# Light must be transformed as well
		glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0)) 
			
		# Render the map
		# chessboard.render()
		camera1.render();
		camera2.render();
	
		# Show the screen
		pygame.display.flip()
