from __future__ import print_function
import cv2
import numpy as np

bins = np.arange(256).reshape(256,1)

def hist_curve(im):
	h = np.zeros((300,256,3))
	if len(im.shape) == 2:
		color = [(255,255,255)]
	elif im.shape[2] == 3:
		color = [ (255,0,0),(0,255,0),(0,0,255) ]
	for ch, col in enumerate(color):
		hist_item = cv2.calcHist([im],[ch],None,[256],[0,256])
		cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
		hist=np.int32(np.around(hist_item))
		pts = np.int32(np.column_stack((bins,hist)))
		cv2.polylines(h,[pts],False,col)
	y=np.flipud(h)
	return y
	
def hist_lines(im):
	h = np.zeros((300,256,3))
	if len(im.shape)!=2:
		print("hist_lines applicable only for grayscale images")
		im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	hist_item = cv2.calcHist([im],[0],None,[256],[0,256])
	cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
	hist=np.int32(np.around(hist_item))
	for x,y in enumerate(hist):
		cv2.line(h,(x,0),(x,y),(255,255,255))
	y = np.flipud(h)
	return y
	
if __name__ == '__main__':
	import sys
	if len(sys.argv)>1:
		fname = sys.argv[1]
	else:
		fname = 'placa.jpg'
		print("usage : python hist.py <image_file>")
	im = cv2.imread(fname)
	
	if im is None:
		print('Failed to load image file:', fname)
		sys.exit(1)
		
	gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	
	cv2.imshow('image',im)
	while True:
		k = cv2.waitKey(0)&0xFF
		if k == ord('a'):
			curve = hist_curve(im)
			cv2.imshow('histogram',curve)
			cv2.imshow('image',im)
			print('a')
		elif k == 27:
			print('ESC')
			cv2.destroyAllWindows()
			break
	
	
	cv2.destroyAllWindows()