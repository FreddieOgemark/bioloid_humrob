try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time
import math
import cpg.bioloid_network

clientID = -1

deltaTime = 0.01
# Shoulders should point downwards by default!
jointIndices = [15,13,9,12,14,16,1,2] #declared outside of function!
jointOffsets = [0.0,0.0,0.0,0.0,0.0,0.0,-math.radians(90.0),math.radians(90.0)]

# joint and robot handles
pivotHandle = -1
shoulderRightHandle = -1
shoulderLeftHandle = -1
hipRightHandle = -1
hipLeftHandle = -1
jointHandles = []
torsoHandle = -1

def connect_to_vrep():
    global clientID
    global pivotHandle
    global shoulderRightHandle
    global shoulderLeftHandle
    global hipRightHandle
    global hipLeftHandle
    global jointHandles
    global torsoHandle

    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 1000, 5)
    if clientID == -1:
        print('Failed to connect to VREP.')
    else:
        print('Connected to VREP.')
    # Get handles
    _, pivotHandle = vrep.simxGetObjectHandle(clientID, 'Pivot', vrep.simx_opmode_oneshot_wait)
    _, shoulderRightHandle = vrep.simxGetObjectHandle(clientID, 'Joint3', vrep.simx_opmode_oneshot_wait)
    _, shoulderLeftHandle = vrep.simxGetObjectHandle(clientID, 'Joint4', vrep.simx_opmode_oneshot_wait)
    _, hipRightHandle = vrep.simxGetObjectHandle(clientID, 'Joint7', vrep.simx_opmode_oneshot_wait)
    _, hipLeftHandle = vrep.simxGetObjectHandle(clientID, 'Joint8', vrep.simx_opmode_oneshot_wait)

    jointHandles = []
    for i in jointIndices:
        _, h = vrep.simxGetObjectHandle(clientID, 'Joint' + str(i), vrep.simx_opmode_oneshot_wait)
        jointHandles.append(h)
    _, torsoHandle = vrep.simxGetObjectHandle(clientID, 'Bioloid', vrep.simx_opmode_oneshot_wait)
    print('Object handles received.')
    vrep.simxSynchronous(clientID, True)


def disconnect_from_vrep():
    vrep.simxSynchronous(clientID, False)
    vrep.simxFinish(clientID)
    print('Disconnected from VREP.')

def evaluate_individual(weightMatrix):
    print('Evaluating individual...')

    if clientID == -1:
        # This means that the instance was not initialised! 
        raise ValueError("The V-REP instance was not initialised!")
    else:
        # Get handles
        #_, pivotHandle = vrep.simxGetObjectHandle(clientID, 'Pivot', vrep.simx_opmode_oneshot_wait)
        #_, shoulderRightHandle = vrep.simxGetObjectHandle(clientID, 'Joint3', vrep.simx_opmode_oneshot_wait)
        #_, shoulderLeftHandle = vrep.simxGetObjectHandle(clientID, 'Joint4', vrep.simx_opmode_oneshot_wait)
        #_, hipRightHandle = vrep.simxGetObjectHandle(clientID, 'Joint7', vrep.simx_opmode_oneshot_wait)
        #_, hipLeftHandle = vrep.simxGetObjectHandle(clientID, 'Joint8', vrep.simx_opmode_oneshot_wait)

        #jointHandles = []
        #for i in jointIndices:
        #    _, h = vrep.simxGetObjectHandle(clientID, 'Joint' + str(i), vrep.simx_opmode_oneshot_wait)
        #    jointHandles.append(h)

        #print('Object handles received.')

        # Get bioloid handle
        #_, torsoHandle = vrep.simxGetObjectHandle(clientID, 'Bioloid', vrep.simx_opmode_oneshot_wait)

        # Start simulation
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
        print('Sim started. clientID: ' + str(clientID))

        # Speed up simulation
        vrep.simxSetIntegerParameter(clientID, vrep.sim_intparam_speedmodifier, 10, vrep.simx_opmode_oneshot_wait)

        # Set initial joint angles
        for i in range(0,len(jointHandles)):
            vrep.simxSetJointPosition(clientID, jointHandles[i], jointOffsets[i], vrep.simx_opmode_oneshot_wait)
            vrep.simxSetJointTargetPosition(clientID, jointHandles[i], jointOffsets[i], vrep.simx_opmode_oneshot_wait)

        # Set joints that are not considered by the optimizaton
        shoulderAngle = math.radians(80.0)
        vrep.simxSetJointPosition(clientID, shoulderRightHandle, shoulderAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, shoulderRightHandle, shoulderAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointPosition(clientID, shoulderLeftHandle, -shoulderAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, shoulderLeftHandle, -shoulderAngle, vrep.simx_opmode_oneshot_wait)

        hipAngle = math.radians(45.0)
        vrep.simxSetJointPosition(clientID, hipRightHandle, -hipAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, hipRightHandle, -hipAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointPosition(clientID, hipLeftHandle, hipAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, hipLeftHandle, hipAngle, vrep.simx_opmode_oneshot_wait)

        # Evaluate for a number of integration steps
        position = 0
        maxPosition = 0
        _, lastPos = vrep.simxGetObjectPosition(clientID, torsoHandle, -1, vrep.simx_opmode_oneshot_wait)

        bn = cpg.bioloid_network.BioloidNetwork(weightMatrix, deltaTime)
        for iteration in range(0,200):
            # CPG network step
            jointAngles = bn.get_output()

            # Set joint angles
            for i in range(0,len(jointHandles)):
                vrep.simxSetJointTargetPosition(clientID, jointHandles[i], jointOffsets[i] + jointAngles[i], vrep.simx_opmode_oneshot)

            # VREP simulation step
            vrep.simxSynchronousTrigger(clientID)

            # Measure how far forward the robot moves in this timestep
            if iteration % 10 == 0:
                # Measure delta (current - last position)
                _, currPos = vrep.simxGetObjectPosition(clientID, torsoHandle, -1, vrep.simx_opmode_oneshot_wait)
                delta2D = [currPos[0]-lastPos[0], currPos[1]-lastPos[1]]
                lastPos = currPos

                # Measure forward vector
                _, currLocalPos = vrep.simxGetObjectPosition(clientID, torsoHandle, pivotHandle, vrep.simx_opmode_oneshot_wait)           
                forward2D = [ currLocalPos[1], -currLocalPos[0] ]
                forward2DLength = math.sqrt(forward2D[0]*forward2D[0]+forward2D[1]*forward2D[1])

                if forward2DLength == 0.0:
                    forward2D = [0.0, 0.0]
                else:
                    forward2D = [forward2D[0]/forward2DLength, forward2D[1]/forward2DLength]

                # What is the distance along the forward vector?
                forwardDistance = delta2D[0]*forward2D[0]+delta2D[1]*forward2D[1]
                position += forwardDistance
                maxPosition = max(position, maxPosition)

        # Measure movement
        print('Last known position: ' + str(position))
        print('Max position (fitness):' + str(maxPosition))

        # Stop simulation
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        print('Sim stopped.')
        

    print('Done.')
    return maxPosition

#evaluate_individual(bioloid_network.get_random_weights(8,8))
