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

def evaluate_individual():
    print('Evaluating individual...')

def test():
    vrep.simxFinish(-1)
    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 1000, 5)

    if clientID != -1:
        # Get joint handles
        jointIndices = [15,13,9,12,14,16,1,2]
        handles = []

        for i in jointIndices:
            _, h = vrep.simxGetObjectHandle(clientID, 'Joint' + str(i), vrep.simx_opmode_oneshot_wait)
            handles.append(h)
        print('Joint handles received.')

        # Start simulation
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
        vrep.simxSynchronous(clientID, True)
        print('Sim started.')

        for i in range(0,100):
            # CPG network step
            output = [0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0]

            # Set joint angles
            for i in range(0,len(handles)):
                vrep.simxSetJointTargetPosition(clientID, handles[i], output[i], vrep.simx_opmode_oneshot)

            # VREP simulation step
            vrep.simxSynchronousTrigger(clientID)

        # Stop simulation
        vrep.simxSynchronous(clientID, False)
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        vrep.simxFinish(clientID)
        print('Sim stopped.')

# uncomment the following line to test
test()