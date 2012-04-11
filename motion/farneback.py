import cv2
import numpy as np



def dummy(x):
	print x

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

if __name__ == "__main__":

	camera = cv2.VideoCapture(0)

	prevImg = camera.read()[1]
	prevImg = cv2.cvtColor(prevImg,cv2.cv.CV_RGB2GRAY)

	cv2.namedWindow("panel",cv2.cv.CV_WINDOW_NORMAL)
	cv2.cv.MoveWindow("panel",prevImg.shape[1],int(prevImg.shape[0]*1.5))
	
	cv2.createTrackbar("pyr_scale","panel",0,3,dummy)
	cv2.createTrackbar("levels","panel",1,3,dummy)
	cv2.createTrackbar("winsize","panel",5,100,dummy)
	cv2.createTrackbar("iterations","panel",5,10,dummy)
	cv2.createTrackbar("poly_n","panel",0,1,dummy)
	cv2.createTrackbar("flags","panel",0,1,dummy)

	while True:

		nextImg = camera.read()[1]
		nextImg = cv2.cvtColor(nextImg,cv2.cv.CV_RGB2GRAY)

		flow = cv2.calcOpticalFlowFarneback(prevImg, nextImg, None,
			1/pow(2,cv2.getTrackbarPos("pyr_scale","panel")+1),
			cv2.getTrackbarPos("levels","panel"),
			cv2.getTrackbarPos("winsize","panel"),
			cv2.getTrackbarPos("iterations","panel"),
			5+(2*cv2.getTrackbarPos("poly_n","panel")),
			(1.1,1.5)[cv2.getTrackbarPos("poly_n","panel")],
			(cv2.OPTFLOW_USE_INITIAL_FLOW,cv2.OPTFLOW_FARNEBACK_GAUSSIAN)[cv2.getTrackbarPos("flags","panel")]) 

		prevImg = np.copy(nextImg)

		cv2.imshow("flow",draw_flow(nextImg,flow))

		if (cv2.waitKey(5)!=-1):
			break
