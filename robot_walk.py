#from lib_robotis import *
#from usbscan import *

import time
import math
import cpg.bioloid_network
from robot_control.lib_robotis import *
from robot_control.usbscan import *
import file_Operation


def evaluate_individual(genomeFileName):
    f = fileOperations(genomeFileName)
    genome = f.showContent()
    bioloid = bioloid_control.BioloidControl();

    if bioloid.devName:
        deltaTime = 0.01

        # Shoulders should point downwards by default!
        jointIndices = [14,12,8,11,13,15,0,1]
        jointOffsets = [0.0,0.0,0.0,0.0,0.0,0.0,-math.radians(90.0),-math.radians(90.0)]

        # Get handles
        #_, pivotHandle = vrep.simxGetObjectHandle(clientID, 'Pivot', vrep.simx_opmode_oneshot_wait)
        shoulderRightIdx = 2 #joint3
        shoulderLeftIdx = 3 #joint4

        print('Object handles received.')

        # Get bioloid handle
        #_, torsoHandle = vrep.simxGetObjectHandle(clientID, 'Bioloid', vrep.simx_opmode_oneshot_wait)

        # Start simulation
        #vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
        #vrep.simxSynchronous(clientID, True)
        #print('Sim started.')

        # Speed up simulation
        #vrep.simxSetIntegerParameter(clientID, vrep.sim_intparam_speedmodifier, 10, vrep.simx_opmode_oneshot_wait)

        # Set initial joint angles
        for i in range(0,len(jointHandles)):
            bioloid.setJointPosition(jointIndices[i], jointOffsets[i])

        # Set joints that are not considered by the optimizaton
        shoulderAngle = math.radians(80.0)
        bioloid.setJointPosition(shoulderRightIdx, shoulderAngle)
        bioloid.setJointPosition(shoulderLeftIdx, shoulderAngle)

        # Evaluate for a number of integration steps
        position = 0
        maxPosition = 0
        #lastPos = vrep.simxGetObjectPosition(clientID, torsoHandle, -1, vrep.simx_opmode_oneshot_wait)

        bn = cpg.bioloid_network.BioloidNetwork(genome, deltaTime)
        for iteration in range(0,200):
            # CPG network step
            jointAngles = bn.get_output()

            # Set joint angles
            for i in range(0,len(jointHandles)):
                bioloid.setJointPosition(jointIndices[i], jointOffsets[i] + jointAngles[i])

            # move robot
            bioloid.move()

        # Stop robot (TODO : unnecessary here?)

    print('Done.')
    

class Bioloid:
    def __init__(self, usbPort=None):
        self.dev_name = usbPort if usbPort else scan_for_usb()
        self.dyn = USB2Dynamixel_Device(self.dev_name)
        self.servos = []
        self.servoAngle = []
        for i in range(1,19):
            servo = Robotis_Servo(self.dyn,i)
            self.servos.append(servo)
            self.servoAngle.append[0]

    def setJointPosition(self, idx, position):
        self.servoAngle[idx] = position

    def move(self):
        vel = math.radians(100.0)
        # Base-pose:
        for i in range(len(self.servos)):
            servos[i].move_angle(self.servoAngle[i], vel, True) # True here means block call until movement done


#evaluate_individual('2015-10-02_13-41-35_bestGenome.csv')
