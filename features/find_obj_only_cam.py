import numpy as np
import cv2
from common import anorm
from functools import partial
import time

help_message = '''SURF image match 

USAGE: press SPACEBAR to capture first image
       press ENTER to go to the capture mode
'''

FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing

flann_params = dict(algorithm = FLANN_INDEX_KDTREE,
                    trees = 4)

def match_bruteforce(desc1, desc2, r_threshold = 0.75):
    res = []
    for i in xrange(len(desc1)):
        dist = anorm( desc2 - desc1[i] )
        n1, n2 = dist.argsort()[:2]
        r = dist[n1] / dist[n2]
        if r < r_threshold:
            res.append((i, n1))
    return np.array(res)

def match_flann(desc1, desc2, r_threshold = 0.6):
    flann = cv2.flann_Index(desc2, flann_params)
    idx2, dist = flann.knnSearch(desc1, 2, params = {}) # bug: need to provide empty dict
    mask = dist[:,0] / dist[:,1] < r_threshold
    idx1 = np.arange(len(desc1))
    pairs = np.int32( zip(idx1, idx2[:,0]) )
    return pairs[mask]

def draw_match(img1, img2, p1, p2, status = None, H = None):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
    vis[:h1, :w1] = img1
    vis[:h2, w1:w1+w2] = img2
    vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    if H is not None:
        corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
        corners = np.int32( cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) )
        cv2.polylines(vis, [corners], True, (255, 0, 0),thickness=3)
    
    if status is None:
        status = np.ones(len(p1), np.bool_)
    green = (0, 255, 0)
    red = (0, 0, 255)
    for (x1, y1), (x2, y2), inlier in zip(np.int32(p1), np.int32(p2), status):
        col = [red, green][inlier]
        if inlier:
            cv2.line(vis, (x1, y1), (x2+w1, y2), col)
            cv2.circle(vis, (x1, y1), 2, col, -1)
            cv2.circle(vis, (x2+w1, y2), 2, col, -1)
        else:
            r = 2
            thickness = 3
            cv2.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
            cv2.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
            cv2.line(vis, (x2+w1-r, y2-r), (x2+w1+r, y2+r), col, thickness)
            cv2.line(vis, (x2+w1-r, y2+r), (x2+w1+r, y2-r), col, thickness)
    return vis


if __name__ == '__main__':
	captureTriggered = True;
	key = -1;
	
	rectSize = (240,320);
	
	print help_message;
	
	img1 = None;
	
	cam = cv2.VideoCapture(0);
	surf = cv2.SURF(3000)
	while True:
		
		before = time.time()
		f,img2 = cam.read()
		cv2.imshow("original",img2)
		img2 = cv2.cvtColor(img2,cv2.cv.CV_RGB2GRAY)    
		
		if captureTriggered:
			cx,cy = int(img2.shape[1]/2),int(img2.shape[0]/2);
			cv2.rectangle(img2,(cx-rectSize[0]/2,cy-rectSize[1]/2),(cx+rectSize[0]/2,cy+rectSize[1]/2),255);
			cv2.imshow("Capture",img2);
			if (key == 32):
				img1 = img2[cy-rectSize[1]/2:cy+rectSize[1]/2,cx-rectSize[0]/2:cx+rectSize[0]/2];
				captureTriggered = not captureTriggered;
		else:		
			kp1, desc1 = surf.detect(img1, None, False)
			kp2, desc2 = surf.detect(img2, None, False)
			desc1.shape = (-1, surf.descriptorSize())
			desc2.shape = (-1, surf.descriptorSize())
			#print 'img1 - %d features, img2 - %d features' % (len(kp1), len(kp2))
		
			def match_and_draw(match, r_threshold):
					m = match(desc1, desc2, r_threshold)
					matched_p1 = np.array([kp1[i].pt for i, j in m])
					matched_p2 = np.array([kp2[j].pt for i, j in m])        
					if len(matched_p1) >= 4 : # needed because findHomography produces an error
							H, status = cv2.findHomography(matched_p1, matched_p2, cv2.RANSAC, 5.0)
							#print '%d / %d  inliers/matched' % (np.sum(status), len(status))
					else:
							H, status = None, None
					vis = draw_match(img1, img2, matched_p1, matched_p2, status, H)
					return vis
		
			#print 'bruteforce match:',
			#vis_brute = match_and_draw( match_bruteforce, 0.75 )
			#print 'flann match:',
		
			vis_flann = match_and_draw( match_flann, 0.6 ) # flann tends to find more distant second
															# neighbours, so r_threshold is decreased
			#cv2.imshow('find_obj SURF', vis_brute)
			fps = 1/(time.time()-before)
			cv2.putText(img=vis_flann, text=str(fps)+" fps", org=(50, 50), 
						fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
						color=(0, 0, 0), thickness = 2, linetype=cv2.CV_AA)  
			cv2.imshow('find_obj SURF flann', vis_flann)
		key = cv2.waitKey(5)
		
		if (key == 10):
			captureTriggered = True;
		elif (key == 27 or key == 113):
			break;
