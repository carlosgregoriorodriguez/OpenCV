#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
          
if __name__ == "__main__":

	img = cv2.imread("../img/beach.jpg")

	imgR = cv2.split(img)[0]
	imgG = cv2.split(img)[1]
	imgB = cv2.split(img)[2]

	#modify an image so the merge is different
	blurredB = cv2.blur(imgB,(100,100))

	#cv2.imshow("blurredB",blurredB)

	mv = (imgR,imgG,blurredB)

	print mv

	cv2.imshow("merge",cv2.merge(mv))
	cv2.imshow("original",img)

	while True:
		if (cv2.waitKey(5) != -1):
			break
