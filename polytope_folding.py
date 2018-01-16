#!/usr/bin/python3
from scipy.optimize import minimize
import numpy as np
from math_python3 import rotation_transform3 as rt3
import math

def rt(theta,v,a,of):
	"""numpy wrapper of rotation_transform3
	theta: rotation angle
	v: vector of rotation axis
	a: origin of rotation axis
	of: vector of rotated 3d point
	"""
	return np.array(rt3(theta,v,a,of))

def f(t):
	"""coorinates of vertices after folding t"""
	v1 = np.array([-0.5,-2-0.5,0])
	v2 = np.array([0.5,-2-0.5,0])
	v3 = np.array([0.5,-1-0.5,0])
	v4 = np.array([0.5,-0.5,0])
	v5 = np.array([1+0.5,-0.5,0])
	v6 = np.array([1+0.5,0.5,0])
	v7 = np.array([0.5,0.5,0])
	v8 = np.array([0.5,1+0.5,0])
	v9 = np.array([-0.5,1+0.5,0])
	v10 = np.array([-0.5,0.5,0])
	v11 = np.array([-1-0.5,0.5,0])
	v12 = np.array([-1-0.5,-0.5,0])
	v13 = np.array([-0.5,-0.5,0])
	v14 = np.array([-0.5,-1-0.5,0])

	thetaV13V4 = t[0]
	thetaV14V3 = t[1]
	thetaV1V3 = t[2]
	thetaV4V7 = t[3]
	thetaV5V15 = t[4]
	thetaV8V13 = t[5]
	thetaV8V16 = t[6]
	thetaV13V10 = t[7]
	thetaV11V13 = t[8]
	
	v15 = (v7+v6)/2
	v16 = (v9+v10)/2

	v3r = rt(thetaV13V4,v13-v4,v4,v3)
	v14r = rt(thetaV13V4,v13-v4,v4,v14)
	v1r = rt(thetaV14V3,v14r-v3r,v3r,rt(thetaV13V4,v13-v4,v4,v1))
	v2r = rt(thetaV1V3,v1r-v3r,v3r,rt(thetaV14V3,v14r-v3r,v3r,rt(thetaV13V4,v13-v4,v4,v2)))
	v5r = rt(thetaV4V7,v4-v7,v7,v5)
	v15r = rt(thetaV4V7,v4-v7,v7,v15)
	v6r = rt(thetaV5V15,v5r-v15r,v15r,rt(thetaV4V7,v4-v7,v7,v6))
	v16r = rt(thetaV8V13,v8-v13,v13,v16)
	v10r = rt(thetaV8V13,v8-v13,v13,v10)
	v9r = rt(thetaV8V16,v8-v16r,v16r,rt(thetaV8V13,v8-v13,v13,v9))
	v11r = rt(thetaV13V10,v13-v10r,v10r,rt(thetaV8V13,v8-v13,v13,v11))
	v12r = rt(thetaV11V13,v11r-v13,v13,rt(thetaV13V10,v13-v10r,v10r,rt(thetaV8V13,v8-v13,v13,v12)))

	return np.array([v1r,v2r,v3r,v4,v5r,v6r,v7,v8,v9r,v10r,v11r,v12r,v13,v14r,v15r,v16r])

def sed(v1,v2):
	"""squared Euclidean distance
	between np.array (point) v1 and v2
	"""
	return sum((v1-v2)**2)

def dist(v):
	"""sum of the squared distances between glued vertices"""
	return sed(v[9-1],v[7-1])+sed(v[16-1],v[15-1])+sed(v[6-1],v[10-1])+sed(v[5-1],v[3-1])+sed(v[2-1],v[10-1])+sed(v[12-1],v[14-1])+sed(v[1-1],v[11-1])

def normalize_angle(theta):
	"""nomalize radian angle to -Pi <= theta <= Pi"""
	t = math.fmod(theta,2*math.pi)
	if t > math.pi: return -(math.pi-(t-math.pi))
	if t < -math.pi: return math.pi-(-math.pi-t)
	return t

t0 = [0]*9
#print(dist(f(t0)))
result = minimize(lambda t: dist(f(t)), t0, method='Nelder-Mead', tol=1e-15, options={'maxiter':100000, 'disp':True})
print([normalize_angle(t) for t in result.x])

