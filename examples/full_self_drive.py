# Thread 1 - Scan Env, return to Thread 2 for any obstacle < 50
# Thread 2 - Object Mapping, Route Calaculation
# Thread 3 - Navigation, and Thread 1
# Thread 4 - Scan Camera, Look for traffic signals


import picar_4wd as fc
import threading
import concurrent.futures
import navigation as nav
import object_mapping as om
import math
import astar
import logging
import queue


class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=10)
        #self.navigation_lock = threading.Lock()
        #self.obj_map_lock = threading.Lock()
        #super(FullSelfDrive, self).__init__()
        #self.obstacle_event = obstacle_event
        #self.navigation_event = navigation_event
        #self.navigation_lock.acquire()

    def set_grid(self, grid):
        logging.debug("%s:about to add to queue")
        self.put(grid)
        logging.debug("%s:added to queue")

    def get_grid(self):
        logging.debug("%s:about to get from queue")
        value = self.get()
        logging.debug("%s:got %d from queue")
        return value


        

def scan_env(scan_event, navigate_event):
    print("Inside Scan_env")
    scan_event.wait()
    #print("scan_event = ", scan_event.is_set())
    while True:
        #print("Inside full_self.drive.scan_event() - Scanning Started")
        scan_list = fc.scan_step(1.5*om.cell_size, om.cell_size*0.75)
        if not scan_list or len(scan_list) < 10:
            continue
        #scan_list = scan_list[::-1]
        #tmp = scan_list[2:8]
        #tmp = [0,2,1,1]
        if not scan_event.is_set():
            break
        print(scan_list)
        if any(ele != 2 for ele in scan_list):
            print("Scan going to end")
            navigate_event.set()
            break
    
def navigate(navigate_event, scan_event, start_cell, end_cell):
    #global count_scan
    print("Thread Navigate Started")
    #print("Inside full_self_drive.navigate(): Going to call om.map_obstacles_to_grid_v2(start_cell), start_cell = ", start_cell)
    grid = om.map_obstacles_to_grid_v2(start_cell)
    print("Object mapping finished grid = ")
    #count_scan = True

    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in grid]))
    
    
    cost = 1 
    path, directions, results = astar.search(grid, cost, start_cell, end_cell)
    print("Proposed Route through the grid =  ")
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in results]))

    print("start cell = ", start_cell)
    print("end cell = ", end_cell)

    print("path =", path)

    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in path]))
    print(" \n")
    
    
    #path, directions = astar.main()
    #print("Setting Scan Event")
    scan_event.set()
    #print("scan_event = ", scan_event.is_set())
    end_position = nav.move_car(path, directions, navigate_event)
    #scan_event.set()
    
    print("end_position = ", end_position)
    if end_position == end_cell:
        print("destination reached")
        return None, True
    else:
        print("scanning again")
        return end_position, False

def scan_and_navigate():
    global count_scan
    start_cell = om.shape[1] - 1, math.trunc(om.x_init/om.cell_size)
    print("start_cell = ", start_cell)
    end_cell = (0,0)
    """
    print("before creating the navigation thread")
    navigation_thread = threading.Thread(target = navigate, args = (start_cell, end_cell))
    print("before creating the scanning thread")
    scan_thread = threading.Thread(target=scan_env, args = ())
    print("before starting the navigation thread")
    navigation_thread.start()
    print("before starting the scanning thread")
    scan_thread.start()
    navigation_thread.join()
    count_scan = False
    scan_thread.join()
    """

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_object_map = executor.submit(om.map_obstacles_to_grid)
        result_object_map = future_object_map.result()
        
        future_navigation = executor.submit(navigate, start_cell, end_cell)
        future_scan = executor.submit(scan_env)
        return_scan = future_scan.result()
        print("return_scan", return_scan)
        return_navigation = future_navigation.result()
        print("return_navigation", return_navigation)

if __name__ == '__main__':
    try:
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        logging.getLogger().setLevel(logging.DEBUG)
        pipeline = Pipeline()
        #obstacle_event = threading.Event()

        start_cell = om.shape[1] - 1, math.trunc(om.x_init/om.cell_size)
        print("start_cell = ", start_cell)
        end_cell = (0,3)
        destination_reached = False

        navigate_event = threading.Event()
        scan_event = threading.Event()

        while not destination_reached:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                #obstacle mapper updates the grid
                #navigate consumes the grid
                #print("scan_event = ", scan_event.is_set())
                future_scan = executor.submit(scan_env, scan_event, navigate_event)
                future_navigation = executor.submit(navigate, navigate_event, scan_event, start_cell, end_cell)
                end_position, destination_reached = future_navigation.result()
                print("destination_reached = ", destination_reached)
                if destination_reached:
                    print("The threads must end now")
                    fc.stop()
                    navigate_event.set()
                    scan_event.clear()
                    future_scan.cancel()
                    future_navigation.cancel()
                    exit

                else:
                    print("end_position = ", end_position)
                    start_cell = end_position
                    scan_event.clear()
                    navigate_event.clear()
            #om.absolute_angle = 0
            #navigate_event = None
            #scan_event = None

            

            
    #wri    te a catch here.
    finally: 
        fc.stop()


    