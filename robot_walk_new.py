import itertools
import time
import math

import file_operation
import pypot.dynamixel
import cpg.bioloid_network

class BioloidControl:
    servoMinLimits = [  -145,
                        -125,
                        -60,
                        -85,
                        -30,
                        -40,
                        -55,
                        30,
                        0,
                        0,
                        -80,
                        -20,
                        -90,
                        0,
                        -20,
                        -80,
                        -30,
                        -30 ]

    servoMaxLimits = [  125,
                        145,
                        85,
                        60,
                        40,
                        30,
                        -30,
                        55,
                        0,
                        0,
                        20,
                        80,
                        0,
                        90,
                        80,
                        20,
                        30,
                        30 ]

    def __init__(self, initServoSpeed):
        # Connect to bioloid
        print('Connecting to bioloid robot...')
        ports = pypot.dynamixel.get_available_ports()
        print('Available ports: ', ports)

        if not ports:
            raise IOError('No port available!')

        print('Using the first on the list...')
        self.dxl_io = pypot.dynamixel.DxlIO(ports[0], 1000000)
        time.sleep(0.01)
        print('Connected to robot!')

        print('Scanning for all servos...')
        found_ids = self.dxl_io.scan([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
        time.sleep(0.01)
        print('Found servo ids:', found_ids)

        if len(found_ids) != 18:
            raise IOError('Not all 18 servos were found!')

        # Enable servo torque
        self.ids = found_ids
        self.dxl_io.enable_torque(self.ids)
        time.sleep(0.01)

        # Set initial servo speeds
        speeds = dict(zip(self.ids, itertools.repeat(initServoSpeed)))
        self.setServoSpeeds(speeds)

        print('BioloidControl initialized.')

    def disconnect(self):
        print('Disconnecting from robot...')
        self.dxl_io.disable_torque(self.ids)
        time.sleep(0.01)
        self.dxl_io.close()
        time.sleep(0.01)

    def setServoSpeeds(self, speeds):
        self.dxl_io.set_moving_speed(speeds)
        time.sleep(0.01)

    def setServoTargets(self, positions, delay = True):
        # note: positions is a dictionary

        # Clamp target positions to valid range
        clampedPositions = {}

        for servoID, pos in positions.iteritems():
            pos = max(pos, self.servoMinLimits[servoID-1])
            pos = min(pos, self.servoMaxLimits[servoID-1])
            clampedPositions[servoID] = pos

        # Set positions
        self.dxl_io.set_goal_position(clampedPositions)

        if delay:
            time.sleep(0.01)

    def moveToBasePose(self):
        print('Moving to base pose...')
        positions = {   1: 0.0,
                        2: 0.0,
                        3: 0.0,
                        4: 0.0,
                        5: 0.0,
                        6: 0.0,
                        7: -45.0,
                        8: 45.0,
                        9: 0.0,
                        10: 0.0,
                        11: 0.0,
                        12: 0.0, 
                        13: 0.0,
                        14: 0.0,
                        15: 0.0,
                        16: 0.0,
                        17: 0.0,
                        18: 0.0 }

        self.setServoTargets(positions)

        # Wait for movement to complete
        time.sleep(4.0)

def run(genomeDir):
    print('Loading genome...')
    f = file_operation.fileOperations(genomeDir)
    genome = f.getContent()

    robot = BioloidControl(120) # INITIAL SPEED IS SET HERE
    robot.moveToBasePose()

    # Run
    print('Setting up run...')
    deltaTime = 0.01

    # # Shoulders should point downwards by default!
    jointIndices = [15,13,11,12,14,16,1,2]
    jointOffsets = [0.0,0.0,0.0,0.0,0.0,0.0,-math.radians(90.0),math.radians(90.0)]

    # Set initial joint angles
    output = []
    for i in range(0,len(jointIndices)):
        output.append(math.degrees(jointOffsets[i]))
    robot.setServoTargets(dict(zip(jointIndices, output)))

    # Set shoulder servos (that are not considered by the animation)
    shoulderAngle = 70.0
    robot.dxl_io.set_goal_position({ 3: -shoulderAngle, 4: shoulderAngle })
    time.sleep(2.0)

    # Evaluate for a number of integration steps
    print('Starting run!')
    bn = cpg.bioloid_network.BioloidNetwork(genome, deltaTime)

    for iteration in range(0,2000):
        startTime = time.clock()

        # CPG network step
        jointAngles = bn.get_output()

        # Set joint angles
        output = []
        for i in range(0,len(jointIndices)):
            output.append(math.degrees(jointOffsets[i] + jointAngles[i]))
        robot.setServoTargets(dict(zip(jointIndices, output)), False)

        # Wait until next timestep
        updateTime = time.clock() - startTime
        
        time.sleep(deltaTime - updateTime)

    print('Run ended!')

    robot.disconnect()
    print('Done.')

if __name__ == '__main__':
    run('walkingPatterns')