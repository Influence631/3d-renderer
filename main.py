import pygame
import numpy as np
from math import sin, cos
from matrices import rotate_x, rotate_y, rotate_z, projection_matrix, v3_v2, rot_mat
from shapes_calculations import *
pygame.init()
import math
running = True
screen_width = 900
screen_height = 500
scale = 170
angle = 0
radius = 170
total_points = 50
fps = 60


screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()

cube_points = [[0,0,0], [1,0,0], [1,1,0], [0,1,0],
		  [0,0,1], [1,0,1], [1,1,1], [0,1,1]]

COLORS = [
  (255,93,0), (0,215,25), (63,0,255),
  (8,6,51), (255,0,123), (0,219,22),
]

def generate_sphere_points(radius,total_points):
	sphere_points = []
	for i in range(total_points):   
		lat = map(i, 0 , total_points, -np.pi * 0.5, np.pi * 0.5)
		for j in range(total_points):
			lon = map(j, 0, total_points, -np.pi, np.pi)
			x = (radius * sin(lon) * cos(lat))
			y = (radius * sin(lon) * sin(lat))
			z = (radius * cos(lon))
			sphere_points.append([x, y, z])
	return sphere_points #returns an array of points of a sphere using a parametric equation on a sphere


def draw_sphere(points, offset):
	#rotation
	rot_mat_y = rotate_y(angle)
	rot_mat_x = rotate_x(angle)
	rot_mat_z = rotate_z(angle)
	for point in points:
		rotated_point = rot_mat_y.dot(point)
		rotated_point = rot_mat_x.dot(rotated_point)
		rotated_point = rot_mat_z.dot(rotated_point)
		
		projected_point = projection_matrix.dot(rotated_point)
		position = [projected_point[0] + offset[0], projected_point[1] + offset[1]]
		pygame.draw.circle(screen, (255,255,255), position, 3, 3)
		
def draw_line(start_index, end_index, points):
	pygame.draw.line(screen, (255, 255, 255), (points[start_index][0], points[start_index][1]), (points[end_index][0], points[end_index][1]), 5)
	

def draw_cube(projected_vertices):
	face_data = []
	for idx, face_idxs in enumerate(cube_faces):
		# get the rotated 3D points for this frame
		pts3d = [ rot_mat(angle).dot(cube_points[i]) for i in face_idxs ]
		# avg Z = depth
		depth = sum(p[2] for p in pts3d) / len(pts3d)
		face_data.append((depth, idx, face_idxs))

	# 2) sort by depth descending (farthest first)
	face_data.sort(key=lambda x: x[0], reverse=True)

	# 3) draw in that order
	for depth, idx, face_idxs in face_data:
		pts2d = [projected_vertices[i] for i in face_idxs]
		cx = sum(x for x,y in pts2d)/4
		cy = sum(y for x,y in pts2d)/4
		pts2d.sort(key=lambda p: math.atan2(p[1]-cy, p[0]-cx))
		pygame.draw.polygon(screen, COLORS[idx], pts2d)

	
def calculate_cube_faces(cube_vertices):
	faces = []
	for axis in (0,1,2):
		for side in (0,1):
			# collect the indices (0–7) where that coord == side
			face = [i for i, v in enumerate(cube_vertices) if v[axis] == side]
			faces.append(face)
	return faces

			
			


sphere_points = generate_sphere_points(radius, total_points)
cube_faces = calculate_cube_faces(cube_points)
while running:
	angle += 0.01
	for event in pygame.event.get():
		if event.type == pygame.QUIT:   
			running = False
	
	screen.fill((105, 230, 54))
 
	projected_points = calculate_cube_vertices(cube_points, (screen_width * 0.75, screen_height * 0.4),screen, angle, scale)
	draw_cube(projected_points)
	
	draw_sphere(sphere_points, (screen_width * 0.25, screen_height * 0.5))
	
	print(clock.get_fps())
	pygame.display.flip()
	clock.tick(fps)
	
pygame.quit()


