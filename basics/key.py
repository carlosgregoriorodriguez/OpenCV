import cv2
import numpy as np
print "Press a key...";
img = np.zeros((640,480,1));
while True:
	key = cv2.waitKey(100);
	cv2.imshow('Key',img);
	if (key != -1):
		print "Keycode: "+str(key);
		break;
