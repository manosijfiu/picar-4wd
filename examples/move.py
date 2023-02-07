import picar_4wd as fc
import time
import threading
import object_mapping as om
from picar_4wd import Speed




speed_static = 31.35 #speed = cm/second
cell_side_length = om.cell_size
power = 30

    
def move_left():
    global cell_side_length
    fc.turn_left(power)
    om.absolute_angle -= 90
    print("Inside navigation.move_car(), direction taken = left")
    time.sleep(1.50)
    fc.forward(power)
    time.sleep(cell_side_length*1.10/speed_static)
def move_right():
    fc.turn_right(power)
    om.absolute_angle += 90
    print("Inside navigation.move_car(), direction taken = right")
    time.sleep(1.00)
    fc.forward(power)
    time.sleep(cell_side_length*1.10/speed_static)
def move_forward():
    fc.forward(power)
    time.sleep(cell_side_length/speed_static)
def move_backward():
    fc.forward(power)
    time.sleep(cell_side_length/speed_static)

if __name__ == '__main__':
    try:

        move_forward()
        move_left()
        move_right()

    #write a catch here.
    finally: 
        fc.stop()


