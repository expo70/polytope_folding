#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
edge-to-edge gluing algorithm
"""
import sys
import json

class polytopeError(Exception):
	pass

# Latin cross
sample_shape1 = {
	'edges':  [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	'angles': [90,90,180,270,90,90,270,90,90,270,90,90,270,180]
}
sample_shape2 = {
	'edges': [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	'angles': [90,180,90,180,180,180,270,180,90,180,90,180,270,180,90,180,90,180,270,180,90,180,90,180,270,180,180,180]
}
sample_shape3 = {
	'edges': [1,1,1,1,1,1,1,1,1,1],
	'angles': [36,252,36,252,36,252,36,252,36,252] 
}

g_n_solutions = 0
g_output_string = ""

def edge_indices(i1,i2):
	"""adjust the indices of edges (+1) for reading
	"""
	return (i1+1,i2+1)

def print_matches(matches):
	"""print edge-to-edge glues
	"""
	global g_n_solutions
	global g_output_string
	g_n_solutions = g_n_solutions + 1
	g_output_string = g_output_string + "{0:02d}: {1}".format(g_n_solutions, [edge_indices(*m) for m in matches]) + "\n"

def divide_shape(start_edge_no, shape):
	edges = shape['edges']
	angles = shape['angles']
	if len(edges) != len(angles):
		raise polytopeError("Edge and angle numbers do not match.")
	if len(edges)%2 != 0:
		raise polytopeError("Edge and angle numbers should be even.")
	if len(edges) == 0:
		raise polytopeError("Input shape is empty.")
	for i in range(1,len(edges),2):
		if edges[i] != edges[0]: continue
		
		is_p1_ok = False
		is_p2_ok = False
		
		p1_edges = edges[1:i]
		if len(p1_edges) > 0:
			p1_angles = angles[1:i]
			p1_angles[0] = angles[1]+angles[i]
			if p1_angles[0] > 360: continue
			else: is_p1_ok = True
		
		p2_edges = edges[i+1:len(edges)]
		if len(p2_edges) > 0:
			p2_angles = angles[i+1:len(edges)]
			p2_angles[0] = angles[0]+angles[i+1]
			if p2_angles[0] > 360: continue
			else: is_p2_ok = True
		
		divided = []
		if is_p1_ok:
			divided.append({'start_index': start_edge_no+1, 'shape': {'edges':p1_edges, 'angles':p1_angles}})
		if is_p2_ok:
			divided.append({'start_index': start_edge_no+i+1, 'shape': {'edges':p2_edges, 'angles':p2_angles}})
		yield {'glue': (start_edge_no, start_edge_no+i), 'divided': divided}

def glue_and_divide(shapes, matches, depth, max_depth):
	if depth == max_depth:
		print_matches(matches)
		return
	# try to divide the first dividable shape
	for i in range(0,len(shapes)):
		if shapes[i]['shape']==[]: continue
		results = divide_shape(shapes[i]['start_index'], shapes[i]['shape'])
		is_divided = False
		for r in results:
			is_divided = True
			matches.append(r['glue'])
			shapes1 = shapes[0:i]
			shapes1.extend(r['divided'])
			shapes1.extend(shapes[i+1:len(shapes)])
			glue_and_divide(shapes1, matches, depth+1, max_depth)
			matches.pop()
		if is_divided: break
	
def main():
	global g_output_string
	try:
		data = sys.stdin.read()
		if len(data) > 0:
			input_shape = json.loads(data)
	
			shapes0 = [{'start_index': 0, 'shape': input_shape}]
			glue_and_divide(shapes0, [], 0, len(shapes0[0]['shape']['edges'])//2)
	except polytopeError as err:
		g_output_string = "Error: {0}".format(err)
	except ValueError as err:
		g_output_string = "Input value error: {0}".format(err)
	
	print("Content-type: application/json")
	print("\n\n")
	print(json.JSONEncoder().encode({'text': g_output_string}))
	print("\n")

if __name__ == '__main__':
	main()

