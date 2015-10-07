from lib_robotis import *
from usbscan import *

import time

dev_name = '/dev/ttyUSB0' #scan_for_usb()
dyn = USB2Dynamixel_Device(dev_name)

servos = []

for i in range(1,19):
    servo = Robotis_Servo(dyn,i)
    servos.append(servo)

# Read servos
for i in range(0,len(servos)):
    s = servos[i]
    print('Servo ' + str(i+1) + ': ' + str(s.read_angle() * 180.0 / math.pi))

def move():
    vel = math.radians(100.0)
    # Base-pose:
    servos[0].move_angle(0.0, vel, True) # True here means block call until movement done
    servos[1].move_angle(0.0, vel, True)
    servos[2].move_angle(0.0, vel, True)
    servos[3].move_angle(0.0, vel, True)
    servos[4].move_angle(0.0, vel, True)
    servos[5].move_angle(0.0, vel, True)
    servos[6].move_angle(-45.0*math.pi/180.0, vel, True)
    servos[7].move_angle(45.0*math.pi/180.0, vel, True)
    servos[8].move_angle(0.0, vel, True)
    servos[9].move_angle(0.0, vel, True)
    servos[10].move_angle(0.0, vel, True)
    servos[11].move_angle(0.0, vel, True)
    servos[12].move_angle(0.0, vel, True)
    servos[13].move_angle(0.0, vel, True)
    servos[14].move_angle(0.0, vel, True)
    servos[15].move_angle(0.0, vel, True)
    servos[16].move_angle(0.0, vel, True)
    servos[17].move_angle(0.0, vel, True)

    # Stop servos
    time.sleep(1)

    for s in servos:
        s.disable_torque()

#move()

print('Done.')