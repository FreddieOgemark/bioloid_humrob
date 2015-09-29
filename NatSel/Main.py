from GenAlg import GenAlg
from TestFunctionClass import TestFunctionClass
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

print ('Trying to connect to V-REP')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote V-REP API server')
else:
    print ('ERROR!!! COULD NOT CONNECT TO REMOTE API SERVER!!!')

#####################################################################################
robotNameID = "dr12_robot_#"
functionClass = TestFunctionClass()

ga = GenAlg(robotNameID, functionClass)


