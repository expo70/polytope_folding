"""
Mathematica-like functions in python3
"""
import itertools
import math

def delete_duplicates(ls):
	return [item for item,_ in itertools.groupby(sorted(ls))]


def partition(ls, n, disp=None):
	if disp==None:
		return [ls[i:i+n] for i in range(0,len(ls)-(n-1),n)]
	else:
		return [ls[i:i+n] for i in range(0,len(ls)-(n-1),disp)]

def flatten1(ls):
	result = []
	for item in ls: result.extend(item)
	return result

def list_depth(L):
	return isinstance(L,list) and max(map(list_depth, L))+1

def flatten(x):
	"""
	only works in Python3
	"""
	result = []
	for el in x:
		if hasattr(el, "__iter__") and not isinstance(el, (str, bytes)):
			result.extend(flatten(el))
		else:
			result.append(el)
	return result

def all_n(ls, n):
	"""Mathematica ls[[All,n]]
	"""
	return [row[n] for row in ls]

def rotation_transform3(theta,v,a,of):
	(vx,vy,vz) = v
	(ax,ay,az) = a
	(x,y,z) = of
	(vx2,vy2,vz2) = (vx**2,vy**2,vz**2)
	vsq = vx2+vy2+vz2
	vsqr = math.sqrt(vsq)
	return [(-(ay*vx*vy) + ax*vy2 - az*vx*vz + ax*vz2 + vx2*x + vx*vy*y + vx*vz*z + (ay*vx*vy + az*vx*vz - ax*(vy2 + vz2) +          vy2*x + vz2*x - vx*vy*y - vx*vz*z)*       math.cos(theta) - vsqr*       (az*vy - ay*vz + vz*y - vy*z)*math.sin(theta))/    vsq,        (ay*vx2 - ax*vx*vy - az*vy*vz + ay*vz2 +       vx*vy*x + vy2*y + vy*vz*z +       (ax*vx*vy + az*vy*vz - ay*(vx2 + vz2) -          vx*vy*x + vx2*y + vz2*y - vy*vz*z)*       math.cos(theta) + vsqr*       (az*vx - ax*vz + vz*x - vx*z)*math.sin(theta))/    vsq,        (az*vx2 + az*vy2 - ax*vx*vz - ay*vy*vz +       vx*vz*x + vy*vz*y + vz2*z +       (-(az*(vx2 + vy2)) + ax*vx*vz + ay*vy*vz -          vx*vz*x - vy*vz*y + vx2*z + vy2*z)*       math.cos(theta) - vsqr*       (ay*vx - ax*vy + vy*x - vx*y)*math.sin(theta))/    vsq]




