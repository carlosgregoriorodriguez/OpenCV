import cv2
import numpy as np

if __name__ == "__main__":
	img =  cv2.imread("../img/road.jpg");
	print img.shape;
	
	
	h = np.zeros((300,256,3));
	b,g,r = img[:,:,0],img[:,:,1],img[:,:,2]
	bins = np.arange(257)
	bin = bins[0:-1]
	color = [ (255,0,0),(0,255,0),(0,0,255) ]
	
	for item,col in zip([b,g,r],color):
		N,bins = np.histogram(item,bins)
		v=N.max()
		N = np.int32(np.around((N*255)/v))
		N=N.reshape(256,1)
		pts = np.column_stack((bin,N))
		print pts
		print [pts]
		print "aaa"
		print [pts][0]
		print "falla aqui"
		cv2.polylines(h,[pts],False,col,2)
		print "falla aqui"

	
	h=np.flipud(h)
	
	cv2.imshow('img',h)
	cv2.waitKey(0)


		
