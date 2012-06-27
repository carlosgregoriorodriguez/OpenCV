import SimpleCV
from SimpleCV.Features.Detection import Circle
import time
import math
from scipy import spatial
from heatmap import Heatmap, Point

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

display = SimpleCV.Display()
vc = SimpleCV.VirtualCamera("video.mts", "video")
next_key = ord('a')
prev_key = ord('z')
reset_key = ord('r')
plus_scale = ord('m')
less_scale = ord('n')
level = 0
scale = .75
next_scale = scale/4.
painting = False
last_level = None
wasps_masks = []
blobs = []
normalmode = True
while not display.isDone():
	before = time.time()
	display.checkEvents()
	key =  SimpleCV.pg.key.get_pressed()
	init_level = False
	if key[next_key]:
		level += 1
	elif key[prev_key]:
		level -= 1
	
	if key[plus_scale]:
		scale += .05
		resize = True
	elif key[less_scale]:
		scale -= .05
		resize = True
	else: resize = False

	reset = bool(key[reset_key])
	init_level = last_level!=level or reset

	if resize:
		img = init_img.scale(scale)

	if init_level:
		print "Going to level %d"%level
	last_level = level
	if level == 0:
		init_img = vc.getImage()
		img = init_img.scale(scale)
		img.show()
	elif level == 1:
		if init_level:
			img.clearLayers()
			wasps_masks = []
			# last_img = img.copy()
		if display.mouseLeft:
			painting = not painting
			if painting:
				print "Start painting"
				wasplayer = SimpleCV.DrawingLayer(img.size())
				wasplayer.setDefaultAlpha(100)
				wasps_masks.append(wasplayer)
				img.addDrawingLayer(wasplayer)
				color = SimpleCV.Color.getRandom(SimpleCV.Color())
			else:
				print "Stop painting"
		if painting and wasps_masks:
			index = len(wasps_masks)-1
			wasps_masks[-1].circle((display.mouseRawX, display.mouseRawY), int(34*scale), filled=True, color=color)
		img.show()
	elif level==2:
		if init_level:
			img.clearLayers()
			base_img = img.copy()
			blobs = []
			mask = SimpleCV.Image(img.size())
			for i, wasplayer in enumerate(wasps_masks):
				temp_img = SimpleCV.Image(img.size())
				temp_img.addDrawingLayer(wasplayer)
				temp_img = temp_img.applyLayers()
				mask = mask | temp_img
				blob = (temp_img.findBlobs() or [None])[0]
				if blob:
					blob._img = temp_img
					blob._circles = []
					blob.image = img
					blobs.append(blob)
			
			# for wasplayer in wasps_masks: mask.addDrawingLayer(wasplayer)
			# mask = mask.applyLayers().binarize().invert()
			masked_img = img.applyBinaryMask(mask.dilate(int(45*scale)))
			circles = masked_img.smooth('median').findCircle(thresh=200)
			blobs = SimpleCV.FeatureSet(blobs)
			print "Finded blobs",blobs
			print "Finded circles", circles
			if not circles: continue
			for circle in circles:
				for blob in blobs:
					if blob._img[circle.x,circle.y][0]:
						circle.image = img
						blob._circles.append(circle)
						break
			for blob in blobs:
				blob._circles = SimpleCV.FeatureSet(blob._circles)
				blob._selected_circle = None
			if circles:
				#circles.filter(circles.area()<100)
				circle = circles[0]
				
				
				#smoothed_img = masked_img.smooth(aperature=(25,25))
				#smoothed_img.dl.circle(circles.)
				#smoothed_img.show()
				#blobs[0].show()
			else:
				pass
				#blobs[0].show()
				#level = 1
		elif blobs:
			img.clearLayers()
			overlap = blobs.sortDistance((display.mouseRawX, display.mouseRawY))
			#.overlaps((display.mouseRawX, display.mouseRawY,10))
			for blob in blobs: blob.drawOutline()
			blob = overlap[0]
			blob.draw(alpha=100)
			if blob._circles:
				circles = blob._circles.sortDistance((display.mouseRawX, display.mouseRawY))
				for i, circle in enumerate(circles):
					if circle == blob._selected_circle: continue
					elif i==0:
						if display.mouseLeft:
							blob._selected_circle = circle
						color = SimpleCV.Color.BLUE
					else: color = SimpleCV.Color.YELLOW
					circle.draw(color=color)
			if display.mouseRight:
				blob._selected_circle = Circle(img, display.mouseRawX, display.mouseRawY,int(14*scale))
			try:
				blob._selected_circle.draw(color=SimpleCV.Color.RED,width=3)
				blob.drawMinRect(color=SimpleCV.Color.YELLOW, width=2)
			except:
				pass
			img.show()
				# img.applyBinaryMask(blob._img).show()


			#if circles:

	elif level>=3:
		if init_level:
			smoothed = base_img.smooth(aperature=(5,5))
			blob_i = 0
			for blob in blobs: 
				try:
					blob._selected_circle.image = smoothed
					blob._last_position = (int(blob._selected_circle.x/scale), int(blob._selected_circle.y/scale))
					size = init_img.size()
					blob._heatmap = Heatmap(size[0],size[1])
				except:
					pass
		else:
			rc_img = None
			img = vc.getImage()
			smoothed_img = img.scale(next_scale).smooth(aperature=(3,3))

			if display.mouseRight:
				normalmode = not normalmode
			
			positions = []
			for blob in blobs:
				# print "LAST POSItiON", blob._last_position
				# print "LAST: ",blob._last_position,
				positions.append(blob._last_position)
				p = Point(blob._last_position[0],blob._last_position[1])
				blob._heatmap.addPoint(p,30)
				circle = blob._selected_circle
				#circle.x,circle.y = blob._last_position
				color = circle.meanColor()
				color = color[2],color[1],color[0]
				blob._new_img = smoothed_img.colorDistance(color).invert().dilate(1).binarize(235,255)
				rc_img = blob._new_img.copy() if not rc_img else blob._new_img & rc_img
			
			new_blobs = rc_img.invert().findBlobs() or []
			new_positions = []
			for blob in new_blobs:
				a, b = blob.centroid()
				a, b = float(a)/next_scale, float(b)/next_scale
				# print "NEXT", a,b
				new_positions.append((int(a),int(b)))
			try:
				tree = spatial.KDTree(new_positions)
				near_points = tree.query_ball_point(positions,80)
				for i, point in enumerate(near_points):
					# print point, new_positions, len(new_positions)
					if point:
						p = int(point[0])
						# print "POINT", p
						blobs[i]._last_position = new_positions[p]
			except:
				pass
			if normalmode:
				sm_img = img.scale(scale)
				for blob in blobs:
					pos = blob._last_position
					sm_img.drawCircle((int(pos[0]*scale),int(pos[1]*scale)),18*scale,color=SimpleCV.Color.RED,thickness=2)
				sm_img.show()
			else:
				if display.mouseRight:
					blob_i += 1
				image_heat = blobs[blob_i%len(blobs)]._heatmap.transform()
				# surface = SimpleCV.pg.image.fromstring(image_heat.tostring(), image_heat.size, image_heat.mode)
				heat = SimpleCV.Image(image_heat).scale(scale)
				heat.show()

					#new_blobs.show()

		# if init_level:
		# 	masked_img = img.applyBinaryMask(mask).scale(1./2.)
		# 	#kp, keypoints = masked_img._getRawKeypoints()
		# else:
		# 	img = vc.getImage().scale(scale/2.)
		# 	match = img.findKeypointMatch(masked_img,quality=50.00,minDist=0.15,minMatch=0.01)
		# 	if match:
		# 		print match
		# 	img.show()
			#kp_base, keypoints_base = img._getRawKeypoints()
			#idx,dist = img._getFLANNMatches(keypoints_base,keypoints)
			#print idx,dist
			#keypoints_base.show()