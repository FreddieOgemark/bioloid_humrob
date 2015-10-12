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

def connect_to_vrep():
    global clientID
    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 1000, 5)
    if clientID == -1:
        print('Failed to connect to VREP.')
    else:
        print('Connected to VREP.')

def disconnect_from_vrep():
    vrep.simxFinish(clientID)
    print('Disconnected from VREP.')

def evaluate_individual(weightMatrix):
    print('Evaluating individual...')

    if clientID == -1:
        # This means that the instance was not initialised! 
        raise ValueError("The V-REP instance was not initialised!")
    else:
        deltaTime = 0.01

        # Shoulders should point downwards by default!
        jointIndices = [15,13,11,12,14,16,1,2]
        jointOffsets = [0.0,0.0,0.0,0.0,0.0,0.0,-math.radians(90.0),math.radians(90.0)]

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

        print('Object handles received.')

        # Get bioloid handle
        _, torsoHandle = vrep.simxGetObjectHandle(clientID, 'Bioloid', vrep.simx_opmode_oneshot_wait)

        # Start simulation
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
        vrep.simxSynchronous(clientID, True)
        print('Sim started.')

        # Speed up simulation
        #vrep.simxSetIntegerParameter(clientID, vrep.sim_intparam_speedmodifier, -1, vrep.simx_opmode_oneshot_wait)

        # Set initial joint angles
        for i in range(0,len(jointHandles)):
            vrep.simxSetJointPosition(clientID, jointHandles[i], jointOffsets[i], vrep.simx_opmode_oneshot_wait)
            vrep.simxSetJointTargetPosition(clientID, jointHandles[i], jointOffsets[i], vrep.simx_opmode_oneshot_wait)

        # Set joints that are not considered by the optimizaton
        shoulderAngle = math.radians(80.0)
        vrep.simxSetJointPosition(clientID, shoulderRightHandle, -shoulderAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, shoulderRightHandle, -shoulderAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointPosition(clientID, shoulderLeftHandle, shoulderAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, shoulderLeftHandle, shoulderAngle, vrep.simx_opmode_oneshot_wait)

        hipAngle = math.radians(45.0)
        vrep.simxSetJointPosition(clientID, hipRightHandle, -hipAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, hipRightHandle, -hipAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointPosition(clientID, hipLeftHandle, hipAngle, vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, hipLeftHandle, hipAngle, vrep.simx_opmode_oneshot_wait)

        # Evaluate for a number of integration steps
        position = 0
        maxPosition = 0
        _, lastPos = vrep.simxGetObjectPosition(clientID, torsoHandle, -1, vrep.simx_opmode_oneshot_wait)
        lowestPos = 5 #starting way above
        cumZPos = 0


        bn = cpg.bioloid_network.BioloidNetwork(weightMatrix, deltaTime)
        for iteration in range(0,1200):
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
                lowestPos = min(lowestPos, currPos[2])
                cumZPos += currPos[2]
                #print("cumZPos: " + str(cumZPos))
                if currPos[2] < 0.1:
                    print("ROBOT HAS FALLEN! Torso position z: " + str(currPos[2]))
                    break

        # Measure movement
        print('Last known position: ' + str(position))
        print('Max position (fitness):' + str(maxPosition))
        print('Lowest position:' + str(lowestPos))

        # Stop simulation
        vrep.simxSynchronous(clientID, False)
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        print('Sim stopped.')
        

    print('Done.')
    testFitness = maxPosition*lowestPos
    #print("Cumulative z pos is is " + str(cumZPos))
    #return cumZPos
    return testFitness
    #return maxPosition

#evaluate_individual(bioloid_network.get_random_weights(8,8))
