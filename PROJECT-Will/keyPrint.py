# Prints out the key code
#
# Some basic key codes:
#         SPACE - 32      ENTER - 13      ESC - 27
#         q - 113         a - 97          s - 115
#         UP - 63232      DOWN - 63233    RIGHT - 63235    LEFT - 63234
#         b - 98          c - 99          f - 102

import cv2

if __name__ == '__main__':

	cv2.namedWindow("KEY TEST");

	while True:
		
		key = cv2.waitKey(1000);

		if (key != -1):
			print key;

		if (key == 27 or key == 113):   #to QUIT press ESC or q
			print("quitting ...");
			break;