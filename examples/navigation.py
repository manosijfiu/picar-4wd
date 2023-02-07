
#import time
from keyboard_control import Keyborad_control
import object_mapping as om
import astar
import math
import move
import picar_4wd as fc
from picar_4wd import Speed
from threading import Event


start_cell = om.shape[1] - 1, math.trunc(om.x_init/om.cell_size)
print("start_cell = ", start_cell)
end_cell = (0,0)




def move_car(route_path, directions, navigate_event):
    #directions.pop()
    #print("route_path = ", route_path)
    #print("Inside navigation.move_car(), directions = ", directions)
    #print("Inside navigation.move_car(), primary om.absolute_angle = ", om.absolute_angle)
    direction_in_str = om.get_dir_in_str(om.absolute_angle)
    start_dir = directions[0]
    if direction_in_str == "up":
        if start_dir == 1:
            move.move_forward()
        elif start_dir == 2:
            move.move_left()
        elif start_dir == -2:
            move.move_right()
        elif start_dir == -1:
            move.move_backward()
        else:
            "The Routing Path is not correct"
    elif direction_in_str == "left":
        if start_dir == 1:
            move.move_right()
        elif start_dir == 2:
            move.move_forward()
        elif start_dir == -2:
            move.move_backward()
        elif start_dir == -1:
            move.move_left()
        else:
            "The Routing Path is not correct"
    elif direction_in_str == "down":
        if start_dir == 1:
            move.move_backward()
        elif start_dir == 2:
            move.right()
        elif start_dir == -2:
            move.move_left()
        elif start_dir == -1:
            move.move_forward()
        else:
            "The Routing Path is not correct"
    elif direction_in_str == "right":
        if start_dir == 1:
            move.move_left()
        elif start_dir == 2:
            move.move_forward()
        elif start_dir == -2:
            move.move_backward()
        elif start_dir == -1:
            move.move_right()
        else:
            "The Routing Path is not correct"
    route_path.pop()
    
    print("route_path = ", route_path)
    for i in range(1,len(directions)):
        if navigate_event.is_set():
            print("Navigation is going to be stopped")
            fc.stop()
            break
        #print("Inside navigation.move_car(), direction = ", directions[i])
        move_dir_gap = directions[i] - directions[i - 1] 
        if move_dir_gap == 0:
            move.move_forward()
        elif move_dir_gap == 1:
            if directions[i] > 0:
                move.move_left()
            else:
                move.move_right()
        elif move_dir_gap == -1:
            if directions[i] > 0:
                move.move_right()
            else:
                move.move_left()
        elif move_dir_gap == 3:
            if directions[i] == 1:
                move.move_left()
            else:
                move.move_right()
        elif move_dir_gap == -3:
            if directions[i] == -1:
                move.move_left()
            else:
                move.move_right()
        else:
            "Wrong Direction"
        route_path.pop()
        print("Inside navigation.move_car() route_path = ", route_path)
    #print("Inside navigation.move_car(), final om.absolute_angle  = ", om.absolute_angle)
    
    if len(route_path) > 0:
        return route_path.pop()
    else:
        return "Error: Destination crossed"



#def main(cost_unit, source, target):
def main():
    #grid = om.map_obstacles_to_grid()
    #route_path = astar.search(grid, cost_unit, source, target)

    
    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

    

    start = (9,5)
    end = (0,0)
    #check if end is in obstacle or not
    #print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in grid]))
    
    
    cost = 1 
    path, directions, results = astar.search(grid, cost, start, end)
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in results]))

    #print("start cell = ", start_cell)
    #print("end cell = ", end_cell)

    print("path =", path)

    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in path]))
    print(" \n")
    print("direction = ", directions)
    for i in directions:
        print("Next Direction = ", i)
    
    #path, directions = astar.main()
    navigate_event = Event()
    navigate_event.set()
    end_position = move_car(path, directions, navigate_event)
    if end_position == end_cell:
        print("destination reached")
    else:
        print("scanning again")
    print("end_position = ", end_position)

if __name__ == '__main__':
    try:
        main()
    #write a catch here.
    finally: 
        fc.stop()




