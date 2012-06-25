import numpy as np

# Based on this:
# http://www.monografias.com/trabajos18/gps-solucion/gps-solucion.shtml
# And doesn't seem to work.
# Run gpsmethod.py and press space to capture 4 points

def getPosition(p1,p2,p3,p4,d1,d2,d3,d4):
	x1,y1,z1 = p1;
	x2,y2,z2 = p2;
	x3,y3,z3 = p3;
	x4,y4,z4 = p4;
	
	
	x1 = x1[0]; x2 = x2[0]; x3 = x3[0]; x4 = x4[0];
	y1 = y1[0]; y2 = y2[0]; y3 = y3[0]; y4 = y4[0];
	z1 = z1[0]; z2 = z2[0]; z3 = z3[0]; z4 = z4[0];
	
	arrd = np.array([ \
		[x1-x2,y1-y2,z1-z2], \
		[x2-x3,y2-y3,z2-z3], \
		[x3-x4,y3-y4,z3-z4]]);
	d = np.linalg.det(arrd);
	
	arrx = np.array([ \
		[(d2**2-d1**2)/2, y1-y2, z1-z2], \
		[(d3**2-d2**2)/2, y2-y3, z2-z3], \
		[(d4**2-d3**2)/2, y3-y4, z3-z4]]);
	print "arrx:";
	print arrx;
	x = np.linalg.det(arrx) / d;
	
	arry = np.array([ \
		[x1-x2, (d2**2-d1**2)/2, z1-z2], \
		[x2-x3, (d3**2-d2**2)/2, z2-z3], \
		[x3-x4, (d4**2-d3**2)/2, z3-z4]]);
	print "arry:";
	print arry;
	y = np.linalg.det(arry) / d;
	
	arrz = np.array([ \
		[x1-x2, y1-y2, (d2**2-d1**2)/2], \
		[x2-x3, y2-y3, (d3**2-d2**2)/2], \
		[x3-x4, y3-y4, (d4**2-d3**2)/2]]);
	print "arrz:";
	print arrz;
	z = np.linalg.det(arrz) / d;
	
	return [x,y,z];

	
	
