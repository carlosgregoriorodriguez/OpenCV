import cv2
import numpy as np
print "Press a key...q to finish"
img = np.zeros((640,480,1))
while True:
	key = cv2.waitKey(100)
	cv2.imshow('Key',img)
	if (key != -1):
		print "Keycode: ", key, " ",
		if key < 256 :
			print "Key '", chr(key),"'"
		else:
			print "Key '",chr(key&255),"' Bits: ", bin(key)[2:]
		if key & 255 == 113 : #tecla q
			break
