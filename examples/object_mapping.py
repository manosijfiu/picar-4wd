import picar_4wd as fc
import numpy as np
import math
#import keyboard_control as kbc
import time
#from bresenham import bresenham



shape = (9,9) #Dimention of the Grid
cell_size = 30 #Length of each cell in the grid in cm
grid = np.zeros(shape, dtype = int) #the grid in form of numpy array
absolute_angle = 0 #relative angle of the car facing upward direction
ANGLE_RANGE = 120 #total angle range of the servo
STEP = 12 #angle after which the sensor takes a measurement 
us_step = STEP
angle_distance = [0,0]
current_angle = 0 #current angle of the servo
max_angle = ANGLE_RANGE/2 
min_angle = -ANGLE_RANGE/2
x_init = round((shape[1] - 1)/2,1) * cell_size 
y_init = 0
row_no, column_no = np.shape(grid)
status_list = []
count_scan_step = 0
obstacle_list = []

"""
class Obstacle:
    start = ()
    end = ()
    block_coords = []
    count_point = 0
    def __init__(self, start):
        self.start = tuple(start)
        self.count_point += 1
    def add_end(self, end):
        self.end = tuple(end)
        self.add_block_coords(self.start, self.end)
        self.count_point += 1
    def add_block_coords(self, start, end):
        print("start = ", start)
        print("end = ", end)
        self.block_coords = list(bresenham(start[0], start[1], end[0], end[1]))
    def __str__(self):
        #print("type of return str = ", type("start = " + str(self.start) + " end = " + str(self.end) + " point_count = " + str(self.count_point)))
        return "start = " + str(self.start) + " end = " + str(self.end) + " point_count = " + str(self.count_point) + str(self.block_coords)
    def __repr__(self):
        return self.__str__()
"""
#returns the direction of the face of the car with the absolute angle
def get_dir_in_str(absolute_angle):
    #print ("Inside om.get_dir_in_str(), absolute_angle = ", absolute_angle)
    if absolute_angle % 360 == 0:
        return "up"
    elif absolute_angle % 360 == 90 or absolute_angle % 360 == -270:
        return "right"
    elif abs(absolute_angle % 360) == 180:
        return "down"
    elif absolute_angle % 360 == -90 or absolute_angle % 360 == 270:
        return "left"
    else:
        print("Exception will be raised")
        raise Exception("The angle is illegal")

#returns the current position of the ultrasonic in cm 2d graph with respect to x and y coordinate. (not cell location of the 2d numpy array)
def get_coords(position, dir):
    #print("Inside om.get_coords, dir = ", dir)
    coords = []
    if dir == "up":
        coords.append(int((position[1] + 0.5) * cell_size))
        coords.append(int((row_no - position[0]) * cell_size))
    elif dir == "right":
        coords.append(int((position[1] + 1) * cell_size))
        coords.append(int((row_no - 1 - position[0] + 0.5) * cell_size))
    elif dir == "down":
        coords.append(int((position[1] + 0.5) * cell_size))
        coords.append(int((row_no - 1 - position[0]) * cell_size))
    elif dir == "left":
        coords.append(int((position[1]) * cell_size))
        coords.append(int((row_no - 1 - position[0] + 0.5) * cell_size))
    else:
        print("The direction is illegal")
        raise Exception("The angle is illegal")
    #print("Inside om.get_corrds(), coords = ", coords)
    return coords



def get_obstacle_cells(angle):
    global angle_distance, cell_size
    xcord, ycord = -100, -100
    fc.servo.set_angle(angle)
    time.sleep(0.04)
    dist = fc.us.get_distance()
    #There is no space for the Untrasonic Sensor to connect to the Pi at the bottom because of the Servo.
    #Therefore, we put the Ultrasonic Sensor upside down. This is why the angles are read opposite way
    if angle != 0:
        angle = -angle
    #print("angle = ", angle, " dist = ", dist)
    #print("sin of angle = ", angle, " is = ", math.sin(math.radians(angle)))
    #print("cos of angle = ", angle, " is = ", math.cos(math.radians(angle)))
    #print("original y cord = ", dist * math.cos(math.radians(angle)))
    #print("original x cord = ", dist * math.sin(math.radians(angle)))
    #print("x_init = ", x_init)
    if dist > 0 : #and dist < (3 * cell_size):
        ycord = math.trunc(dist * math.cos(math.radians(angle))/cell_size)
        xcord = math.trunc((dist * math.sin(math.radians(angle))+ x_init)/cell_size)
        #print("Inside get_coordinates : xcord = ", xcord, "ycord = ", ycord)
    if xcord >= 0 and ycord >= 0 and xcord < row_no - 1 and ycord < column_no - 1:
        return tuple([dist, angle, column_no - ycord - 1, xcord])
    else:
        #print("Inside returning False")
        return False


#retrieves the cell location of the obstacles in terms of the grid numpy array
def get_obstacle_cells_v2(angle, last_position):
    global angle_distance, cell_size, absolute_angle
    xcord, ycord = -100, -100
    fc.servo.set_angle(angle)
    time.sleep(0.04)
    dist = fc.us.get_distance()
    angle_distance = {}
    #There is no space for the Untrasonic Sensor to connect to the Pi at the bottom because of the Servo.
    #Therefore, we put the Ultrasonic Sensor upside down. This is why the angles are read opposite way
    angle = -angle
    #print("Inside om.get_obstacle_cells_v2, absolute_angle = ", absolute_angle)
    direction = get_dir_in_str(absolute_angle)
    us_coords = get_coords(last_position, direction)
    #print("Inside om.get_obstacle_cells_v2, direction = ", direction)

    #angle_distance[angle] = 
    #print("Inside om.get_obstacle_cells_v2(), angle = ", angle, " dist = ", dist)
    
    if dist > 0:# and dist < (3 * cell_size):
        #print("Inside om.get_obstacle_cells_v2() sin of angle = ", angle, " is = ", math.sin(math.radians(angle)))
        #print("Inside om.get_obstacle_cells_v2() cos of angle = ", angle, " is = ", math.cos(math.radians(angle)))
        #print("Inside om.get_obstacle_cells_v2() cos cord = ", dist * math.cos(math.radians(angle)))
        #print("Inside om.get_obstacle_cells_v2() sin cord = ", dist * math.sin(math.radians(angle)))
        #print("Inside om.get_obstacle_cells_v2() us_coords[x] = ", us_coords[0])
        #print("Inside om.get_obstacle_cells_v2() us_coords[y] = ", us_coords[1])
        if direction == "up":
            ycord = math.trunc((us_coords[1] + dist * math.cos(math.radians(angle)))/cell_size)
            xcord = math.trunc((us_coords[0] + dist * math.sin(math.radians(angle)))/cell_size)
        elif direction == "right":
            ycord = math.trunc((us_coords[1] + dist * math.cos(math.radians(angle)))/cell_size)
            xcord = math.trunc((us_coords[0] + dist * math.sin(math.radians(angle)))/cell_size)
        elif direction == "down":
            ycord = math.trunc((us_coords[1] - dist * math.cos(math.radians(angle)))/cell_size)
            xcord = math.trunc((us_coords[0] - dist * math.sin(math.radians(angle)))/cell_size)
        elif direction == "left":
            ycord = math.trunc((us_coords[1] + dist * math.sin(math.radians(angle)))/cell_size)
            xcord = math.trunc((us_coords[0] - dist * math.cos(math.radians(angle)))/cell_size)
        #print("Inside om.get_obstacle_cells_v2() : xcord = ", xcord, "ycord = ", ycord)
    if xcord >= 0 and ycord >= 0 and xcord < row_no - 1 and ycord < column_no - 1:
        return tuple([dist, angle, column_no - ycord - 1, xcord])
    else:
        #print("Inside get_obstacle_cells_v2() returning False")
        return False

def scan_step():
    global current_angle, us_step, count_scan_step
    obstacle_list = []
    #print("Inside Scan Step, count_scan_step", count_scan_step)
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    print("calling get_obstacle_cells")
    obstacle_position = get_obstacle_cells(current_angle)#ref1
    if(obstacle_position):
        obstacle_list.append(obstacle_position)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            # print("reverse")
            count_scan_step += 1
            obstacle_list.reverse()
        print("Inside scan_step, obstacle_list:", obstacle_list)
        tmp = obstacle_list.copy()
        obstacle_list = []
        return tmp
    else:
        return False

def scan_step_v2(last_position):
    global current_angle, us_step, count_scan_step, obstacle_list
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    #print("Inside om.scan_step_v2(), current_angle = ", current_angle)
    obstacle_position = get_obstacle_cells_v2(current_angle, last_position)
    #print("Inside om.scan_step_v2(), obstacle_position = ", obstacle_position)#ref1
    #print("Inside om.scan_step_v2(), check obstacle_position, ", bool(obstacle_position))
    if obstacle_position:
        obstacle_list.append(obstacle_position)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            # print("reverse")
            count_scan_step += 1
            obstacle_list.reverse()
        #print("Inside om.scan_step_v2(), obstacle_list:", obstacle_list)
        tmp = obstacle_list.copy()
        obstacle_list = []
        return tmp
    else:
        return False

"""
def get_distance_at(angle):
    global angle_distance
    fc.servo.set_angle(angle)
    time.sleep(0.04)
    distance = us.get_distance()
    angle_distance = [angle, distance]
    return distance
"""


def obstacle_detection(obstacle_readings):
    print("Inside obstacle detection, obstacle_readings = ", obstacle_readings)
    #map_count_false = {}
    len_item = {}
    #obstacles = []

    if len(obstacle_readings) > 0:
        """
        for index, item in enumerate(obstacle_readings):
            print("item = ", item)
            print("item false count = ", item.count(False))
            map_count_false[index] = item.count(False)
        final_obstacle_reading = obstacle_readings[min(map_count_false, key=map_count_false.get)]
        """
        for index, item in enumerate(obstacle_readings):
            #print("item = ", item)
            #print("item size count = ", len(item))
            len_item[index] = len(item)
        final_obstacle_reading = obstacle_readings[max(len_item, key=len_item.get)]
        return final_obstacle_reading
        """
        print("Inside Obstacle Detection: final_obstacle_reading = ", final_obstacle_reading)
        for index, item in enumerate(final_obstacle_reading):
            if not item or index == len(final_obstacle_reading) - 1:
                continue
            print("Inside Obstacle Detection: item = ", item)
            print("Inside Obstacle Detection: index = ", index)
            ##Work with obstacle Append logic.
            print("obstacle length = ", len(obstacles))
            if len(obstacles) == 0:
                obstacles.append(Obstacle([item[2], item[3]]))
            elif final_obstacle_reading[index + 1] and \
                (abs(item[0] - final_obstacle_reading[index + 1][0])) < 5 \
                and abs(item[1] - final_obstacle_reading[index + 1][1]) == STEP:
                obstacles[-1].count_point += 1
                continue
            else:
                print(item, final_obstacle_reading[index + 1])
                if len(obstacles) > 0:
                    obstacles[-1].add_end([item[2],item[3]])
                if final_obstacle_reading[index + 1]:
                    obstacles.append(Obstacle([final_obstacle_reading[index + 1][2], final_obstacle_reading[index + 1][3]]))
        print("Inside obstacle detection, obstacles = ", obstacles)
        return obstacles
        """
    else:
        print("No obstacles detected")
        return False
"""
def obstacle_detection_v2(obstacle_readings):
    print("Inside obstacle detection, obstacle_readings = ", obstacle_readings)
    #map_count_false = {}
    max_len = 0
    final_obstacles = []
    if len(obstacle_readings) > 0:
        for index, obstacle_reading in enumerate(obstacle_readings):
            obstacles = []
            #print("item = ", item)
            #print("item false count = ", item.count(False))
            #map_count_false[index] = item.count(False)
        #final_obstacle_reading = obstacle_readings[min(map_count_false, key=map_count_false.get)]
            print("Inside Obstacle Detection: obstacle_reading = ", obstacle_reading)
            for index, item in enumerate(obstacle_reading):
                if not item or index == len(obstacle_reading) - 1:
                    continue
                print("Inside Obstacle Detection: item = ", item)
                print("Inside Obstacle Detection: index = ", index)
                ##Work with obstacle Append logic.
                print("obstacle length = ", len(obstacles))
                if len(obstacles) == 0:
                    obstacles.append(Obstacle([item[2], item[3]]))
                elif obstacle_reading[index + 1] and \
                    (abs(item[0] - obstacle_reading[index + 1][0])) < 5 \
                    and abs(item[1] - obstacle_reading[index + 1][1]) == STEP:
                    obstacles[-1].count_point += 1
                    continue
                else:
                    print(item, obstacle_reading[index + 1])
                    if len(obstacles) > 0:
                        obstacles[-1].add_end([item[2],item[3]])
                    if obstacle_reading[index + 1]:
                        obstacles.append(Obstacle([obstacle_reading[index + 1][2], obstacle_reading[index + 1][3]]))
            print("Inside obstacle detection, obstacles = ", obstacles)
            ##return 
            if max_len < len(obstacles):
                max_len = len(obstacles)
                final_obstacles = obstacles
        print("Inside obstacle detection, final_obstacles = ", final_obstacles)
        return final_obstacles

    else:
        print("No obstacles detected")
        return False
    """


def map_obstacles_to_grid():
    #print("If you want to quit.Please press q")
    global grid, count_scan_step
    #print("count_scan_step = ", count_scan_step)
    obstacle_readings = []
    #fc.forward(speed)
    while count_scan_step < 2:
        obstacle_list = scan_step()
        if not obstacle_list:
            continue
        #print("length of obstacle_list = ", len(obstacle_list))
        #print("Inside map_obstacles_to_grid() obstacle list = ", obstacle_list)
        obstacle_readings.append(obstacle_list)
        """
        for obstacle_position in obstacle_list:
            if not obstacle_position:
                continue
            grid[obstacle_position[2]][obstacle_position[3]] = 1
        """
        #print(grid[x+x_init][y])
        #key = kbc.readkey()
        #if key=='q':
        #    print("quit")
        #    break
        #else:
        #    continue
    #obstacles = obstacle_detection(obstacle_readings)
    #print("Inside main, obstacles = ", obstacle_readings)
    for obstacles in obstacle_readings:
        for point in obstacles:
            grid[point[2]][point[3]] = 1
    
    #print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in grid]))
    count_scan_step = 0
    return grid

def map_obstacles_to_grid_v2(last_position):
    #print("If you want to quit.Please press q")
    global grid, count_scan_step
    obstacle_readings = []
    while count_scan_step < 4:
        obstacle_list = scan_step_v2(last_position)
        if not obstacle_list:
            continue
        obstacle_readings.append(obstacle_list)
    for obstacles in obstacle_readings:
        for point in obstacles:
                grid[point[2]][point[3]] = 1
    
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in grid]))
    count_scan_step = 0
    return grid

            
        

if __name__ == "__main__":
    try: 
        map_obstacles_to_grid_v2(tuple([8,4]))
    finally: 
        fc.stop()

