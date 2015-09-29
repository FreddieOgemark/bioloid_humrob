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
import bioloid_network

def evaluate_individual():
    print('Evaluating individual...')

    vrep.simxFinish(-1)
    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 1000, 5)
    print('Connected to VREP.')

    if clientID != -1:
        # Get joint handles
        jointIndices = [15,13,9,12,14,16,1,2]
        jointHandles = []

        for i in jointIndices:
            _, h = vrep.simxGetObjectHandle(clientID, 'Joint' + str(i), vrep.simx_opmode_oneshot_wait)
            jointHandles.append(h)
        print('Joint handles received.')

        # Get bioloid handle
        _, torsoHandle = vrep.simxGetObjectHandle(clientID, 'Bioloid', vrep.simx_opmode_oneshot_wait)

        # Start simulation
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
        vrep.simxSynchronous(clientID, True)
        print('Sim started.')

        totalDistance = 0
        _, lastPos = vrep.simxGetObjectPosition(clientID, torsoHandle, -1, vrep.simx_opmode_oneshot_wait)


        weightMatrix = bioloid_network.get_random_weights(8,8)
        bn = bioloid_network.BioloidNetwork(weightMatrix,0.01)
        for iteration in range(0,1000):
            # CPG network step
            #output = [-1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0]
            output = bn.get_output()

            # Set joint angles
            for i in range(0,len(jointHandles)):
                vrep.simxSetJointTargetPosition(clientID, jointHandles[i], output[i], vrep.simx_opmode_oneshot)

            # Measure how far the robot moved every 10th (for now) time step
            if iteration % 10 == 0:
                _, currPos = vrep.simxGetObjectPosition(clientID, torsoHandle, -1, vrep.simx_opmode_oneshot_wait)
                delta = [ currPos[0] - lastPos[0], currPos[1] - lastPos[1] ]
                distance = math.sqrt(delta[0]*delta[0] + delta[1]*delta[1])
                lastPos = currPos
                totalDistance += distance

            # VREP simulation step
            vrep.simxSynchronousTrigger(clientID)

        # Measure movement
        print('Total distance travelled (in any direction): ' + str(totalDistance))

        # Stop simulation
        vrep.simxSynchronous(clientID, False)
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        print('Sim stopped.')
        vrep.simxFinish(clientID)
        print('Disconnected from VREP.')

    print('Done.')
    return totalDistance

evaluate_individual()