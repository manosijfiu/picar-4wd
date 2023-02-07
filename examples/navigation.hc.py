from picar_4wd import Speed
#import time
from keyboard_control import Keyborad_control
import object_mapping as om
import astar
import math
import move
import picar_4wd as fc

current_speed = Speed(25)
current_speed.start()
start_cell = om.shape[1] - 1, math.trunc(om.x_init)
print("start_cell = ", start_cell)
end_cell = None


#navigate without obstacles


def move_car(route_path, directions):
    #directions.pop()
    #print("route_path = ", route_path)
    start_dir = directions[0]
    if start_dir == 1:
        print("start forward")
        move.move_forward()
    elif start_dir == 2:
        print("start left")
        move.move_left()
    elif start_dir == 4:
        print("start right")
        move.move_right()
    elif start_dir == 3:
        print("start back")
        move.move_backward()
    else:
        "The Routing Path is not correct"
    route_path.pop()
    print("route_path = ", route_path)
    for i in range(1,len(directions)):
        print("Inside navigation.move_car()", i)
        move_dir_num = directions[i] - directions[i - 1] 
        if move_dir_num == 0:
            print("continue")
            move.move_forward()
        elif move_dir_num == 1:
            print("turn left")
            move.move_left()
        elif move_dir_num == -1:
            print("turn right")
            move.move_right()
        else:
            "Wrong Direction"
        route_path.pop()
        print("route_path = ", route_path)
    
    if len(route_path) > 0:
        return route_path[0]
    else:
        return "Destination crossed"



#def main(cost_unit, source, target):
def main():
    #grid = om.map_obstacles_to_grid()
    #route_path = astar.search(grid, cost_unit, source, target)

    grid = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    start = (9,5)
    end = (0,0)
    cost = 1 
    path, directions, results = astar.search(grid, cost, start, end)


    print("grid==================================")

    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in grid]))


    print("results================================")
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in results]))

    
    print(" \n")
    print("direction = ", directions)
    for i in directions:
        print("Next Direction = ", i)
    
    #path, directions = astar.main()
    end_position = move_car(path, directions)
    print("end_position = ", end_position)
    exit



if __name__ == '__main__':
    try: 
        main()
    finally: 
        fc.stop()




