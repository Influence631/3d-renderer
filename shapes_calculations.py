from matrices import *
import pygame

def calculate_cube_vertices(points, offset, screen, angle, scale): #pass an array of points
    projected_points = []
    rot_mat_y = rotate_y(angle)
    rot_mat_x = rotate_x(angle)
    rot_mat_z = rotate_z(angle)
    for point in points:
        #apply rotations
        rotated_point = rot_mat_y.dot(point)
        rotated_point = rot_mat_x.dot(rotated_point)
        rotated_point = rot_mat_z.dot(rotated_point)
        
        #project the point
        projected_point = projection_matrix.dot(rotated_point)
        
       
        draw_pos_x = projected_point[0] * scale + offset[0]
        draw_pos_y = projected_point[1] * scale + offset[1]
        
        projected_points.append([draw_pos_x, draw_pos_y])
        
        
        pygame.draw.circle(screen, (255,255,255), (draw_pos_x,  draw_pos_y), 5, 4 )
    
    return projected_points