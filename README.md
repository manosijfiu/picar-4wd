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
 
 
 
 
 







