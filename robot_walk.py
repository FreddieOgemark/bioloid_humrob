import time
import math
import cpg.bioloid_network
from robot_control.lib_robotis import *
from robot_control.usbscan import *
import file_operation

class BioloidControl:
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

    def move(self, postUpdateDelay):
        vel = math.radians(100.0)

        for i in range(len(self.servos)):
            servos[i].move_angle(self.servoAngle[i], vel, False) # True here means block call until movement done

        pause(postUpdateDelay)

def evaluate_individual(genomeFileName):
    f = file_operation.FileOperations(genomeFileName)
    genome = f.showContent()
    bioloid = BioloidControl();

    if bioloid.dev_name:
        deltaTime = 0.01

        # Shoulders should point downwards by default!
        # Join [15,13,9,12,14,16,1,2]
        jointIndices = [14,12,8,11,13,15,0,1]
        jointOffsets = [0.0,0.0,0.0,0.0,0.0,0.0,-math.radians(90.0),-math.radians(90.0)]

        # Get handles
        shoulderRightIdx = 2 # Joint 3
        shoulderLeftIdx = 3 # Joint 4

        # Set initial joint angles
        for i in range(0,len(jointHandles)):
            bioloid.setJointPosition(jointIndices[i], jointOffsets[i])

        # Set joints that are not considered by the optimizaton
        shoulderAngle = math.radians(80.0)
        bioloid.setJointPosition(shoulderRightIdx, shoulderAngle)
        bioloid.setJointPosition(shoulderLeftIdx, shoulderAngle)

        # Wait 5 seconds for the base pose to stabilize
        bioloid.move(5.0)

        # Evaluate for a number of integration steps
        bn = cpg.bioloid_network.BioloidNetwork(genome, deltaTime)
        for iteration in range(0,200):
            # CPG network step
            jointAngles = bn.get_output()

            # Set joint angles
            for i in range(0,len(jointHandles)):
                bioloid.setJointPosition(jointIndices[i], jointOffsets[i] + jointAngles[i])

            # move robot
            bioloid.move(deltaTime)

        # Stop robot (TODO : unnecessary here?)
    print('Done.')

evaluate_individual('genomeData/2015-10-02_15-51-12_bestGenome.csv')
