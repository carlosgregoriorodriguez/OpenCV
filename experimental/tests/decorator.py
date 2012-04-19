from __init__ import *

@processor
def grayscale(img):
	return cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

@processor(blur = Trackbar(1,30))
def blur(img, blur):
	return cv2.blur(img,(blur,)*2)


# @processor(GrayScaleProcessor)
# def complexc(img):
# 	return img

# camview(blur())

camview(blur(),AdaptiveThresholdProcessor(), ContoursProcessor())
