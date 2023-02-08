import picar_4wd as fc
from picar_4wd import Speed
import threading
import time

speed_event = threading.Event()

global_power = 30
speed3 = Speed(25)
speed4 = Speed(4) 

def test():
    global speed_event
    speed3.start()
    speed4.start()
    try:
        # nc.stop()
        speed_event.wait()
        while 1:
            # speed_counter 
            # = 0
            print(speed3())
            print(speed4())
            print(" ") 
            time.sleep(0.5)
    finally:
        speed3.deinit()
        speed4.deinit()
        fc.stop() 
    

def move_car():
    global speed_event
    fc.forward(global_power)
    speed_event.set()
    time.sleep(3)
    speed_event.clear()
    fc.backward(global_power)
    speed_event.set()
    time.sleep(3)
    speed_event.clear()



if __name__ == '__main__':
    try:
        move_thread = threading.Thread(move_car)
        test_thread = threading.Thread(test)
        move_thread.start()
        test_thread.start()
        
    #write a catch here.
    finally: 
        fc.stop()
        speed3.deinit()
        speed4.deinit()


