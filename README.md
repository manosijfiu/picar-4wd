## PiCar-4WD 
PiCar-4WD : This code base I have forked from Sunfounder and I am editting it to have my school project of implementing self driving the resource constraint sunfounder picar. Please do not consider this as copyright violation as I am fully giving all the credits to Sunfounder for the code base. My work is only the changes that I am making for my project and that can be tracked by commit history to this repository.

## Hardwares Needed
Following are the hardware requirements for the project.
1) [Raspberry Pi 4B (4 GB RAM)](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TC2BK1X/)
2) [64 GB microSD](https://www.amazon.com/Samsung-MicroSD-Adapter-MB-ME64GA-AM/dp/B06XX29S9Q/)
3) [Car Chassis Kit](https://www.amazon.com/dp/B087QKRX5J/)
4) [18650 Batteries](https://www.amazon.com/gp/product/B0BCW9Q5QQ/ref=ox_sc_act_title_2?smid=A1OSTWROXS834E&psc=1)
5) [USB Type-C cable and charger](https://www.amazon.com/Raspberry-Model-Official-SC0218-Accessory/dp/B07Z8P61DQ/?pldnSite=1)
6) An external computer monitor
7) [Video display cable](https://www.amazon.com/CanaKit-Raspberry-Micro-HDMI-Cable/dp/B07TTKD38N)
8) A keyboard and a mouse.

## STEP 1 : Set up the Car - Chasis
Please assemble the Sunfounder Robot car using [this link](https://drive.google.com/file/d/1EPBqR5zZ24e2lzKgk8_uIlzh_wIRuezV/view)

## STEP 2: Install the Raspberry Pi
1) First download the image file from [here](https://www.raspberrypi.com/software/)
2) Then please run the imager by following the steps for your recommended OS.
3) Add a wpa_supplicant.conf file to the root of the SD card using the 9
following instructions:
  a. Change the country code from US to your 2-letter ISO 3166-1 country code if not in the USA. Also change the ssid (name of your Wifi network - note this is case sensitive) and psk (your Wifi password)
  b. Sample: 
    ```
    ctrl_interface=DIR=/var/run/wpa_supplicant
    GROUP=netdev
    update_config=1
    country=US
    network={
            ssid="WiFiName"
            psk="WiFiPassword"
            id_str="school"
            priority=0
    }

    ```
 4) Connect the Pi by SSH from your computer.
    
 ## STEP 3: Download the Library
 1) Please download the pi-car library from [here](https://github.com/sunfounder/picar-4wd) into the Pi.
 2)Enter the folder picar-4wd.
 
 ``` 
 
 cd /home/pi/picar-4wd
 
 ```
 3)Then initialize the environment
 ``` 
 
 sudo python3 setup.py install
 
 ```
 
 ## STEP 4: Test your car
 Try to remotely control the car using w,s,d,a,4,5,6, and q after running the following file:

   ```
   
   $ cd /home/pi/picar-4wd/examples 
   $ python3 keyboard_control.py
   
   ```
 
 If your car moves backwards for w and forward for a, please cross-check running the move_forward.py file and check if the car is moving backwards. If it does, that means that the motors are installed other way around. You do not need to disperse, you just need to change the power signs in init file as shown here [__init__.py](https://github.com/manosijfiu/self-driving-pi/blob/master/picar_4wd/__init__.py) and then run the initialize command again. You may have to restart the session after initialize command to reflect the changes in the direction.
 
 ## Step 5: A simple SLAM for avoiding the obstacles
 
The idea is to make the car moving forward and while doing so, the car must scan for obstacles and if any obstacles found, it will make a smart decision to change its direction. If there are obstacles in both forward and right side, the car will take left turn, and right turn for the vice-versa. If there is an obstacle too close, the car will move a little backwards.
 
 Place your car in a surface with random obstacles scattered around. Please run the following command to see how it works. I have also attached a video.
 
 ```
 $ cd /home/pi/picar-4wd/examples
 $ python3 obstacle_avoidance.py
 ```
 
Video Link [Here](https://fiudit-my.sharepoint.com/personal/mroyc001_fiu_edu/_layouts/15/onedrive.aspx?login_hint=mroyc001%40fiu%2Eedu&id=%2Fpersonal%2Fmroyc001%5Ffiu%5Fedu%2FDocuments%2FMobile%2DComputing%2FLab%20Docs%2FReports%2Fobstacle%20avoidance%20%28Rubric%203%2D4%29%20part%204%20redone%2Emp4&parent=%2Fpersonal%2Fmroyc001%5Ffiu%5Fedu%2FDocuments%2FMobile%2DComputing%2FLab%20Docs%2FReports). Please request access.
 
Now, the obstacle avoidance system will need 2 parameters. the first one is for the distance of the obstacles that the car should try to change direction. The second one is for emergency response. This will have the car move a little backward as the obstacle is too near as discovered late. Currently, it has been hardcoded as 35cm and 10cm respectively.

## Step 6: Advanced Mapping

In this step we will see that how the car plots an object into a 2 x 2 grid. This would eventually enable the car in the later steps to automatically reach the dectination avoiding the obstacle mapped in this stage. We assume that the car be in the 9 x 9 grid where every cell is 30cm x 30cm in soze. (We have assumed this size because the picar if of 22cm in width and 25 cm in length). Also, we have assumed that the virtual grid is laid in front of the car where the car is at the bottom middle cell of the 9 x 9 grid i.e. at position (8, 4).

All the cells there in the grid are 0 by default - means they are empty. When the sensor of the car scans the environment, and if any object is found in front of the car, the cells containing the obstacles becomes 1 denoting obstacles. 

Please run the following command and look at the output how it plots the obstacles in the virtual grid.

```
  $ cd /home/pi/picar-4wd/examples
  $ python3 obstacle_mapping.py
```

## Step 7: Auto navigation

In this step, we will pass a virtual grid as an input to the car as a hardcoded value, we will also pass a target cell, and source cell in the 9 x 9 sized grid. Then we will run the navigation.hc.py to see if the car is navigating to the target avoiding all the obstacles (1s in the grid). At first, the car will calculate the shortest path from source to the destination using the astar algorithm implemented in [astar.py](https://github.com/manosijfiu/picar-4wd/blob/master/examples/astar.py), and then it will use ```move_car()``` method of [navigation.hc.py](https://github.com/manosijfiu/picar-4wd/blob/master/examples/navigation.hc.py) to navgate the pi car along with th epath calculated. The path calculated will be shown in the output console.

For example, my pi-car has been given the following grid. The target cell was given as (0, 0) and the source cell was given as (8,5).
```
            [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
```

And the Pi was navigated according to the path shown below **TBA**

 ```
  $ cd /home/pi/picar-4wd/examples
  $ python3 navigation.hc.py
```
 
## Step 8: Full Self Driving

Here, we will combine everything we did independently in Step 5, 6, and 7 and let the pi completely self drive from a source to the destination avoiding all the obstacles including newly discovered obstacles using multi-threading programing in python. The pi will first start with scanning for obstacles of its surrondings and plot the obstacle map in the 9 x 9 grid. However, it will not scan for more than 60cm (2 x cell side length) to avoid errors. Once the obstacle mapping completes, it will take the grid with obstacles into it and generate the shortest path using astar.py. After that it will start moving along with the generated path. All of these are achieved by ```navigate()``` method of the [full_self_drive](https://github.com/manosijfiu/picar-4wd/blob/master/examples/full_self_drive.py). Once it starts its journey towards the destination, it will simultaneously start scanning for new obstacles along the way, and this is taken care by ```scan_env()``` method of the same file. Once the car discovers a new obstacle, the navigate() method returns the last position in the cell, and it starts scanning for the obstacle again. But now the source gets updated to the last position as navigate() method returned previously. The obstacles are mapped using the absolute position of the car and also absolute direction of the car using the ```absolute_angle``` in obstacle_mapping.py.

This multi-threading programming is taken care by the main() method in the same ```full_self_drive.py```. The video of self driving is attached. The source is (8,4) and the destination was kept as (0,3). Watch the video [here](https://fiudit-my.sharepoint.com/personal/mroyc001_fiu_edu/_layouts/15/onedrive.aspx?login_hint=mroyc001%40fiu%2Eedu&id=%2Fpersonal%2Fmroyc001%5Ffiu%5Fedu%2FDocuments%2FMobile%2DComputing%2FLab%20Docs%2FReports%2FLab%201%20Part%202%2FFull%20Self%20Drive%2Emp4&parent=%2Fpersonal%2Fmroyc001%5Ffiu%5Fedu%2FDocuments%2FMobile%2DComputing%2FLab%20Docs%2FReports%2FLab%201%20Part%202) - Please request access.


 ```
  $ cd /home/pi/picar-4wd/examples
  $ python3 full_self_drive.py
```
 
 
 ## Recognizing Objects and responding to it using Machine Learning models.
 
In this last step, we will automate object recognization using the picamera and CNN models like Tensorflow. We will use OpenCV for preprocessing the images and and the inyterpreter api of tensor flow to detect the objects.
 
 1. Please assemble the camera into the Raspberry Pi using [this link](https://www.raspberrypi.com/documentation/accessories/camera.html)
 2. Please follow the steps to use [this link](https://www.tensorflow.org/lite/guide/python) to use Tensorflow Lite with Raspberry Pi.
 3. [This link] can be used for setting up OpenCV on the Raspberry Pi.

Now it is time to test the object detection. At first, we need to print a Stop Sign and put it in front of the Pi. Then we must run ```detect.py``` given by the tensorflow lite library (/home/pi/examples/lite/examples/object_detection/raspberry_pi/detect.py). We also need to connect the Pi to a monitor or install VNC viewer on the computer and connect the Pi from the VNC viewer to be able to see how Pi **sees** and **interprets** the object. Please check our work [here](https://fiudit-my.sharepoint.com/personal/mroyc001_fiu_edu/_layouts/15/onedrive.aspx?login_hint=mroyc001%40fiu%2Eedu&id=%2Fpersonal%2Fmroyc001%5Ffiu%5Fedu%2FDocuments%2FMobile%2DComputing%2FLab%20Docs%2FReports%2FLab%201%20Part%202%2Fstop%20sign%20detection%20preview%2Emp4&parent=%2Fpersonal%2Fmroyc001%5Ffiu%5Fedu%2FDocuments%2FMobile%2DComputing%2FLab%20Docs%2FReports%2FLab%201%20Part%202).


After the preview, we can be sure that the Pi is able to detect the object and now it is time to respond to the object. It can be traffic signs, animals, or humans. But you can also build your own models and train the pi to detect. Now, with this object detection, we have made the Pi stop for 5 seconds whenever a Stop Sign is encountered. The video is [here](https://fiudit-my.sharepoint.com/personal/mroyc001_fiu_edu/_layouts/15/onedrive.aspx?login_hint=mroyc001%40fiu%2Eedu&id=%2Fpersonal%2Fmroyc001%5Ffiu%5Fedu%2FDocuments%2FMobile%2DComputing%2FLab%20Docs%2FReports%2FLab%201%20Part%202%2Fautomatic%20responding%20to%20Stop%20Sign%2Emp4&parent=%2Fpersonal%2Fmroyc001%5Ffiu%5Fedu%2FDocuments%2FMobile%2DComputing%2FLab%20Docs%2FReports%2FLab%201%20Part%202)
We can also extend this functionality to stop and wait until an animal is gone from the way of the Pi.

 ```
  $ cd /home/pi/picar-4wd/examples/examples/object_detection/raspberry_pi
  $ python3 detect.py
```









