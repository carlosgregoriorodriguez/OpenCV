import SimpleCV
import time
import numpy as np
import math

display = SimpleCV.Display()
normaldisplay = False
img_file, center = 'images/wasp1.png', (180,220)
#img_file, center = 'images/wasp.png', (150,240)

img = SimpleCV.Image(img_file)
d = (16,13,14)
#cd = img.colorDistance(c)
#processed = cd.morphGradient()
#processed = cd.binarize(-1,maxv=30)
c = img.getPalette()
#a,b,c = c[0],c[1],c[6]
#print a,b,c
#a,b,c=[15, 11, 13], [51, 41, 41], [106,  94,  96]
#[126 115 121] [33 24 25] [47 36 34]
# processed = img.convolve()

processed = img.convolve().stretch(70,200).dilate(2)

def get_direction(img,center,radius):
	num = 300
	theta = np.linspace(0,2*math.pi,num)
	is_black= False
	black, white = 0, 0
	can_white = False
	black_white = [] #(is_black,theta)
	candidates = []
	for t in theta:
		x = center[0]+radius*math.cos(t)
		y = center[1]+radius*math.sin(t)
		c = img.getPixel(int(x),int(y))[0]
		last_black = t if black>=5 else False
		last_white = t if white>=5 and white<=20 else False
		if c==0:
			if last_white: black_white.append((False,last_white,white))
			black +=1
			white = 0
			processed.dl().circle((x,y),2,SimpleCV.Color.GREEN)
		else:
			if last_black: black_white.append((True,last_black,black))
			black = 0
			white +=1

	if len(black_white)>=3:
		for i in range(len(black_white)-2):
			if black_white[i][0]==black_white[i+2][0]==True and not black_white[i+1][0]:
				old_t = black_white[i+1][1]
				adjusted_t = old_t-(math.pi/num)*black_white[i+1][2]-0.02
				candidates.append(adjusted_t)

	max_r = radius*2.3
	for c in candidates:
		#processed.drawLine(center,(center[0]+ math.cos(c)*r, center[1]+r*math.sin(c)),SimpleCV.Color.BLUE)
		external_point = (int(center[0]+ math.cos(c)*max_r), int(center[1]+max_r*math.sin(c)))
		if img.getPixel(*external_point)[0]==0 or len(candidates)==1:
			return c
			#processed.drawLine(center,external_point,SimpleCV.Color.YELLOW,2)
	return None

scale = 1
r = 50*scale

processed = img.scale(scale).convolve([[1,2],[-1,1]]).dilate(1).stretch(70,200)
# processed.dl().circle(center, r, SimpleCV.Color.RED)
center = list(map(lambda x:x*scale,center))
theta = get_direction(processed,center,r)
if theta:
	external_point = (int(center[0]+ math.cos(theta)*100), int(center[1]+100*math.sin(theta)))
	processed.drawLine(center,external_point,SimpleCV.Color.YELLOW,2)

while not display.isDone():
	if display.mouseRight:
		normaldisplay = not(normaldisplay)

	if normaldisplay:
		img.show()
	else:
		processed.show()
	time.sleep(.1)
# 
# 	before = time.time()
# 	candidates = []

# 	if display.mouseRight:
# 		normaldisplay = not(normaldisplay)

# 	img = vc.getImage().scale(.3) #.flipHorizontal()
# 	for color in colors:
# 		dist = img.colorDistance(color).dilate(2)
# 		segmented = dist.stretch(180,255)
# 		blobs = segmented.findBlobs()
# 		candidates += blobs

# 	if candidates:
# 		#circles = blobs
# 		#circles = candidates.filter([b.isCircle(.8) for b in candidates])
# 		for circle in candidates:
# 			radius = circle.radius()
# 			if radius<=10:
# 				img.drawCircle((circle.x, circle.y), radius,SimpleCV.Color.RED,min(radius,3))
# 	fps = 1/(time.time()-before)

# 	if normaldisplay:
# 		img.drawText('%d fps'%fps,0,0)
# 		img.show()
# 	else:
# 		segmented.show()
