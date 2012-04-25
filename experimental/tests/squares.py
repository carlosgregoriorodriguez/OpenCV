from __init__ import *
import numpy as np
import numpy.linalg as nl
import cv2
import math
def angle( pt1, pt2, pt0 ):
    d1 = pt1[:] - pt0[:]
    d2 = pt2[:] - pt0[:]
    d1 = d1[0]
    d2 = d2[0]
    # print d1,d2,nl.norm(d1),nl.norm(d2)
    return np.dot(d1, d2)/(nl.norm(d1)*nl.norm(d2)+1e-5)


def is_square(contour):
    """
    Squareness checker

    Square contours should:
        -have 4 vertices after approximation, 
        -have relatively large area (to filter out noisy contours)
        -be convex.
        -have angles between sides close to 90deg (cos(ang) ~0 )
    Note: absolute value of an area is used because area may be
    positive or negative - in accordance with the contour orientation
    """
    area = math.fabs( cv2.contourArea(contour) )

    isconvex = cv2.isContourConvex(contour)
    s = 0

    if len(contour) == 4 and area > 1000 and isconvex:

        for i in range(1, 4):
            # find minimum angle between joint edges (maximum of cosine)
            pt1 = contour[i]
            pt2 = contour[i-1]
            pt0 = contour[i-2]
            t = math.fabs(angle(pt0, pt1, pt2))
            if s <= t:s = t

        # if cosines of all angles are small (all angles are ~90 degree) 
        # then its a square
        if s < 0.3:return True

    return False       

def find_squares_from_binary( gray ):
    """
    use contour search to find squares in binary image
    returns list of numpy arrays containing 4 points
    """
    squares = []
    raw_contours, hierarchy = cv2.findContours(gray, cv2.cv.CV_RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in raw_contours:

        arclength = cv2.arcLength(contour,False)
        polygon = cv2.approxPolyDP(contour, arclength * 0.02, True)
        if is_square(polygon):
            squares.append(polygon[0:4])
    return squares

def find_squares4(color_img):
    """
    Finds multiple squares in image

    Steps:
    -Use Canny edge to highlight contours, and dilation to connect
    the edge segments.
    -Threshold the result to binary edge tokens
    -Use cv.FindContours: returns a cv.CvSequence of cv.CvContours
    -Filter each candidate: use Approx poly, keep only contours with 4 vertices, 
    enough area, and ~90deg angles.

    Return all squares contours in one flat list of arrays, 4 x,y points each.
    """
    #select even sizes only
    width, height = color_img.shape[:2]
    timg = color_img.copy() # make a copy of input image

    # select the maximum ROI in the image

    # down-scale and upscale the image to filter out the noise
    timg = cv2.pyrDown( timg )
    timg = cv2.pyrUp( timg ) #, 7

    squares = []

    # Find squares in every color plane of the image
    # Two methods, we use both:
    # 1. Canny to catch squares with gradient shading. Use upper threshold
    # from slider, set the lower to 0 (which forces edges merging). Then
    # dilate canny output to remove potential holes between edge segments.
    # 2. Binary thresholding at multiple levels
    N = 11
    for c in [0]: #[0, 1, 2]
        #extract the c-th color plane
        #tgray = timg[:,:,c]
        gray = cv2.cvtColor(timg,cv2.COLOR_RGB2GRAY)
        #gray = cv2.adaptiveThreshold(gray,120,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,2)
        
        gray = cv2.Canny(gray,threshold1=0,threshold2=50,apertureSize=5)
        gray = cv2.dilate(gray,kernel=None,iterations=1)
        #
        squares = squares + find_squares_from_binary( gray )
        # # Look for more squares at several threshold levels
        for l in range(1, N):
            _, tgray = cv2.threshold(gray, (l+1)*255/N, 255, cv2.THRESH_BINARY )
            #tgray = cv2.adaptiveThreshold(gray,(l+1)*255/N,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,2)
            # cv.Threshold( tgray, gray, (l+1)*255/N, 255, cv.CV_THRESH_BINARY )
            squares = squares + find_squares_from_binary( tgray )

    return color_img, squares


RED = (0,0,255)
GREEN = (0,255,0)
def draw_squares( color_img, squares ):
    """
    Squares is py list containing 4-pt numpy arrays. Step through the list
    and draw a polygon for each 4-group
    """
    color, othercolor = RED, GREEN
    for square in squares:
        cv2.polylines(color_img, [square], True, color, 3, cv2.cv.CV_AA, 0)
        color, othercolor = othercolor, color
    return color_img

@processor
def find_squares(img):
    img, squares = find_squares4( img )
    return draw_squares( img, squares )


# @processor(GrayScaleProcessor)
# def complexc(img):
#   return img

# camview(blur())

camview(find_squares())
