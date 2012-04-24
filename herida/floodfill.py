import cv2
import numpy as np
import sys
from glob import glob



def dummy(x):
	print x


def ffCenter(img,mask):
	y = img.shape[0]
	x = img.shape[1]
	seeds = []
	for px in range(int(x/3),int(2*x/3)+1,int(x/3)):
		for py in range(int(y/3),int(2*y/3)+1,int(y/3)):
			seeds.append((px,py))
	lo = 5
	hi = 5
	for seed in seeds:
		cv2.floodFill(img, mask, seed, (255, 255, 255), (lo,)*3, (hi,)*3)
	return img


def doAndPack(img):
	hueImg = cv2.split(cv2.cvtColor(img, cv2.cv.CV_BGR2HSV))[0]
	h, w = img.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	ffImg = ffCenter(hueImg.copy(),mask)
	background = np.zeros((h,w*3),np.uint8)
	background[0:h,0:w]=cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)
	background[0:h,w:2*w]=hueImg
	background[0:h,2*w:3*w]=ffImg
	return background


if __name__ == "__main__":


	path = 'images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.imread(imageNames[imgIndex])	
	bigImg = doAndPack(img)

	def changeImg(imgName):
		newImg = cv2.imread(imgName)	
		return doAndPack(newImg)

	while True:

		cv2.imshow('original + hue Channel + ff',bigImg)
		
		
		key = cv2.waitKey(5)

	 	if (key==63235):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		bigImg = changeImg(imageNames[imgIndex])
	 	elif (key==63234):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		bigImg = changeImg(imageNames[imgIndex])

	 	elif (key != -1):
	 		break









	