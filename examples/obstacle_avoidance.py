import picar_4wd as fc
import time
from random import randint
speed = 10


def move_decision(scan_list):
    left_free = False
    right_free = False
    print("scan_list[0:3] = ", scan_list[0:3])
    print("scan_list[7:10] = ", scan_list[7:10])
    left_free = True if scan_list[0:3].count(2) > 1 else False
    right_free = True if scan_list[7:10].count(2) > 1 else False
    if left_free and right_free: 
        if scan_list[0:3].count(2) > scan_list[7:10].count(2) >=2 :
            right_free = False
        elif scan_list[0:3].count(2) < scan_list[7:10].count(2) >= 2:
            left_free = False

    if left_free and right_free:
        rand = randint(0,1)
        if rand:
            print("no obs any side random left")
            fc.turn_left(speed)
            time.sleep(0.88)
        else:
            print("no obs any side -  random right ")
            fc.turn_right(speed)
            time.sleep(0.88)
    elif left_free:
        print("no obs left side -  took left ")
        fc.turn_left(speed)
        time.sleep(0.88)
    elif right_free:
        print("no obs right side -  took right ")
        fc.turn_right(speed)
        time.sleep(0.88)
    else:
        print("everything blocked -  backup and scan again ")
        fc.stop()
        fc.backward(speed)
        time.sleep(2)
        main()







def main():
    while True:
        scan_list = fc.scan_step(35,10)
        if not scan_list or len(scan_list) < 10:
            continue
        #scan_list = scan_list[::-1]
        tmp = scan_list[3:7]
        #tmp = [0,2,1,1]
        print(scan_list)
        print(tmp)
        if tmp == [2,2,2,2]:
            print("1st if - straight")
            fc.forward(speed)
        elif tmp == [1,2,2,2]:
            print("2nd if - right")
            fc.turn_right(speed)
            time.sleep(0.5)
        elif tmp == [2,2,2,1]:
            print("3rd if - left")
            fc.turn_left(speed)
            time.sleep(0.5)
        elif 0 in tmp[1:3] and tmp[0] != 2 and tmp[3] == 2:
            print("4th if - back-left")
            fc.backward(speed/2)
            time.sleep(1)
            fc.turn_left(speed)
            time.sleep(0.88)
        elif 0 in tmp[1:3] and tmp[3] != 2 and tmp[0] == 2:
            print("5th if - back right")
            fc.backward(speed/2)
            time.sleep(1)
            fc.turn_right(speed)
            time.sleep(0.88)
        elif 1 in tmp[1:3] and tmp[0] != 2 and tmp[3] == 2:
            print("6th if - central detect, no obs on right align - turn right")
            #fc.backward(speed/2)
            #time.sleep(0.01)
            move_decision(scan_list)
        elif 1 in tmp[1:3] and tmp[3]!= 2 and tmp[0] == 2:
            print("7th if - central detect no obs on left align - turn left")
            #fc.backward(speed/2)
            #time.sleep(0.01)
            move_decision(scan_list)
        elif 1 in tmp[1:3] and tmp[0] == 2 and tmp[3]==2:
            #fc.backward(speed/2)
            #time.sleep(0.05)
            move_decision(scan_list)
        elif 0 in tmp[1:3] and tmp[0] == 2 and tmp[3]==2:
            fc.backward(speed/2)
            time.sleep(1)
            rand = randint(0,1)
            if rand:
                print("8th if - immediate obs - back random left")
                fc.turn_right(speed)
                time.sleep(0.88)
            else:
                print("9th if - immediate obs - back  random right ")
                fc.turn_right(speed)
                time.sleep(0.88)
        elif tmp[0] == 0 and tmp[3] == 2:
            print("12th if - immediate obs, right free - back right")
            fc.stop()
            fc.backward(speed)
            time.sleep(0.8)
            fc.turn_right(speed)
            time.sleep(0.88)
        elif tmp[3] == 0 and tmp[0] == 2:
            print("13th if - immediate obs, left free - back left")
            fc.stop()
            fc.backward(speed)
            time.sleep(0.8)
            fc.turn_left(speed)
            time.sleep(0.88)


            



if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
