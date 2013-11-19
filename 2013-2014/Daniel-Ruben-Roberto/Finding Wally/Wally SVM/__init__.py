__author__ = 'daniel'

import cv2



#Files for haarcascade
#usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml
#usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml
#usr/share/opencv/haarcascades/haarcascade_frontalface_alt_tree.xml
#usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml


img = cv2.imread("wally.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)
#img = cv2.imread("persona.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)
hc = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")
faces = hc.detectMultiScale(img)

for face in faces:
    cv2.rectangle(img, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (255, 0, 0), 3)

cv2.imshow("Wally's face", img)
if cv2.waitKey(0) == 27:
    cv2.destroyWindow("Wally's face")