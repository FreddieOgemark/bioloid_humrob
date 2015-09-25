if (sim_call_type==sim_childscriptcall_initialization) then 
	simSetScriptSimulationParameter(sim_handle_self,'isFinished',"false")
end 

if (sim_call_type==sim_childscriptcall_cleanup) then 
 
end 

if (sim_call_type==sim_childscriptcall_actuation) then

	if (simGetIntegerSignal("desiredRobotCount")==nil) then
		-- desiredRobotCount wasn't set yet. 
		if (dlgHandle==nil) then
			-- ask how many robots are wanted!
			dlgHandle=simDisplayDialog('Robot count','How many robots should participate in the natural selection game?',sim_dlgstyle_input,false,'5')
		end
		if (simGetDialogResult(dlgHandle)==sim_dlgret_still_open) then
			return -- The ok button wasn't clicked yet
		end
		robotCount=tonumber(simGetDialogInput(dlgHandle)) -- We retrieve the input value
		simEndDialog(dlgHandle) -- we end the dialog
		if (robotCount==nil) then
			robotCount=5
		end
		if (robotCount<2) then
			robotCount=2
		end
		simSetIntegerSignal("desiredRobotCount",robotCount) -- we set the number of robots desired
		simSetIntegerSignal("lastRobotRemovalTime",0)
	end
	
	if (firstPass==nil) then
		firstPass=true
		robotCount=simGetIntegerSignal('desiredRobotCount')
		-- Retrieve various handles:
		robotHandle=simGetObjectHandle("dr12_robot_")
		robotCollisionName="dr12_collision_"
		collisionHandle=simGetCollisionHandle(robotCollisionName)
		robotGraphName="dr12_graph_"
		leftJointHandle=simGetObjectHandle("dr12_leftJoint_")
		rightJointHandle=simGetObjectHandle("dr12_rightJoint_")
		sensorJointHandle=simGetObjectHandle("dr12_leftSensorJoint_")
		leftSensorHandle=simGetObjectHandle("dr12_leftSensor_")
		rightSensorHandle=simGetObjectHandle("dr12_rightSensor_")
		userInterfaceHandle=simGetUIHandle("dr12_control_")
		simSetUIButtonLabel(userInterfaceHandle,0,simGetObjectName(robotHandle))
		-- Here we have the button handles of the user interface:
		ui_timePassedH=20
		ui_score=21
		ui_maxSpeed=22
		ui_minSpeed=23
		ui_sweepSpeed=24
		ui_detectionPersistence=25
		ui_detectionDistance=26
		-- Robot state data:
		leftVelocity=0 
		rightVelocity=0
		acceleration=1 
		interWheelDistance=0.164
		wheelRadius=0.043
		sensorRotationVelocity=0
		leftDetectionTime=0
		rightDetectionTime=0
		startTime=simGetSimulationTime()
		travelledDistance=0
		-- The minimum and range of the values to be regulated:
		params_min={0.1,-0.1,5*math.pi/180,-0.1,0.1}
		params_range={0.8,0.2,85*math.pi/180,2,0.7}
		-- We retrieve current parameters:
		navigationParams={tonumber(simGetScriptSimulationParameter(sim_handle_self,'maxSpeed')),
				tonumber(simGetScriptSimulationParameter(sim_handle_self,'minSpeed')),
				tonumber(simGetScriptSimulationParameter(sim_handle_self,'sweepSpeed')),
				tonumber(simGetScriptSimulationParameter(sim_handle_self,'detectionPersistence')),
				tonumber(simGetScriptSimulationParameter(sim_handle_self,'detectionDistance'))}
		-- We select a random parameter and set it to a random value (within its range):
		paramIndex=math.random(5)
		navigationParams[paramIndex]=params_min[paramIndex]+params_range[paramIndex]*math.random()
		-- We set the updated parameters now:
		simSetScriptSimulationParameter(sim_handle_self,'maxSpeed',navigationParams[1])
		simSetScriptSimulationParameter(sim_handle_self,'minSpeed',navigationParams[2])
		simSetScriptSimulationParameter(sim_handle_self,'sweepSpeed',navigationParams[3])
		simSetScriptSimulationParameter(sim_handle_self,'detectionPersistence',navigationParams[4])
		simSetScriptSimulationParameter(sim_handle_self,'detectionDistance',navigationParams[5])
		-- We reset the score to half its value:
		simSetScriptSimulationParameter(sim_handle_self,'score',tonumber(simGetScriptSimulationParameter(sim_handle_self,'score'))/2)
	end
	
	-- We check all scores:
	allScores,scriptHandles=simGetScriptSimulationParameter(sim_handle_all,'score')
	minScore=999999
	maxScore=-1
	for i=1,#allScores,1 do
		currentScore = allScores[i]
		if (minScore>currentScore) then
			minScore=currentScore
			minHandle=scriptHandles[i]
		end
		if (maxScore<currentScore) then
			maxScore=currentScore
			maxHandle=scriptHandles[i]
		end
	end
	
	copyRobot=false
	removeRobot=false
	if (#allScores<robotCount) then
		-- We don't have enough robots, we duplicate the best performer:
		if (simGetScriptHandle()==maxHandle) then
			copyRobot=true
		end
	else
		if (simGetScriptHandle()==minHandle) then
			-- Do we have to remove this robot? (this one is the worst performer)
			if (#allScores>robotCount) then
				removeRobot=true -- yes because we have too many robots
			end
			if (simGetSimulationTime()-simGetIntegerSignal('lastRobotRemovalTime')>10) then
				removeRobot=true -- yes because too much time has passed since we remove one robot
			end
		end
	end
	
--	if (copyRobot) then
--		originalSelection=simGetObjectSelection()
--		simRemoveObjectFromSelection(sim_handle_all)
--		simAddObjectToSelection(sim_handle_single,robotHandle)
--		simCopyPasteSelectedObjects(true)
--		copRob=simGetObjectLastSelection()
--		simRemoveObjectFromSelection(sim_handle_all)
--		simAddObjectToSelection(originalSelection)
--		-- We have to reposition the new robot (the original one has the exact same position):
--		suffix=simGetNameSuffix(simGetObjectName(copRob))
--		originalSuffix=simGetNameSuffix(nil)
--		simSetNameSuffix(-1)
--		newRobotCollisionHandle=simGetCollisionHandle(robotCollisionName.."#"..suffix)
--		simSetNameSuffix(originalSuffix)
--		while (simHandleCollision(newRobotCollisionHandle)>0) do
--			-- we are colliding. We set the position/orientation of the robot to a random value:
--			simSetObjectPosition(copRob,sim_handle_parent,{-2.5+math.random()*5,-2.5+math.random()*5,0})
--			simSetObjectOrientation(copRob,sim_handle_parent,{0,0,math.random()*2*math.pi})
--		end
--		originalSuffix=simGetNameSuffix(nil)
--		simSetNameSuffix(-1)
--		gh=simGetObjectHandle(robotGraphName.."#"..suffix)
--		simSetNameSuffix(originalSuffix)
--		simSetExplicitHandling(gh,1)
--		simResetGraph(gh)
--		simSetExplicitHandling(gh,0)
--	end
	
	
	-- Here we have the basic and very simple navigation algorithm based on 5 parameters and the proximity sensor's readings:
	dt=simGetSimulationTimeStep()
	
	sensorRange=navigationParams[5]
	leftDetectionState,leftDistanceNow=simReadProximitySensor(leftSensorHandle)
	if leftDetectionState~=1 then leftDistanceNow=sensorRange end
	if (leftDistanceNow>sensorRange) then
		leftDistanceNow=sensorRange
	end
	rightDetectionState,rightDistanceNow=simReadProximitySensor(rightSensorHandle)
	if rightDetectionState~=1 then rightDistanceNow=sensorRange end
	if (rightDistanceNow>sensorRange) then
		rightDistanceNow=sensorRange
	end
	
	leftDetectionTime=leftDetectionTime-dt
	rightDetectionTime=rightDetectionTime-dt
	if (leftDetectionTime<=0) or (leftDistanceNow<leftDetectionDistance) then
		leftDetectionDistance=leftDistanceNow
		leftDetectionTime=navigationParams[4] -- persistence
	end
	if (rightDetectionTime<=0) or (rightDistanceNow<rightDetectionDistance) then
		rightDetectionDistance=rightDistanceNow
		rightDetectionTime=navigationParams[4] -- persistence
	end
	
	t=(leftDetectionDistance-0.1)/(sensorRange-0.1)
	desiredRightVelocity=navigationParams[2]*(1-t)+navigationParams[1]*t
	t=(rightDetectionDistance-0.1)/(sensorRange-0.1)
	desiredLeftVelocity=navigationParams[2]*(1-t)+navigationParams[1]*t
	
	-- Now compute the new velocity for the left side:
	if (desiredLeftVelocity>leftVelocity) then
		leftVelocity=leftVelocity+acceleration*simGetSimulationTimeStep()
		if (leftVelocity>desiredLeftVelocity) then
			leftVelocity=desiredLeftVelocity
		end
	else
		leftVelocity=leftVelocity-acceleration*simGetSimulationTimeStep()
		if (leftVelocity<desiredLeftVelocity) then
			leftVelocity=desiredLeftVelocity
		end
	end
	
	-- Now compute the new velocity for the right side:
	if (desiredRightVelocity>rightVelocity) then
		rightVelocity=rightVelocity+acceleration*simGetSimulationTimeStep()
		if (rightVelocity>desiredRightVelocity) then
			rightVelocity=desiredRightVelocity
		end
	else
		rightVelocity=rightVelocity-acceleration*simGetSimulationTimeStep()
		if (rightVelocity<desiredRightVelocity) then
			rightVelocity=desiredRightVelocity
		end
	end
	
	-- Now make the robot move (kinematically):
	linVar=dt*(leftVelocity+rightVelocity)/2.0
	rotVar=dt*math.atan((rightVelocity-leftVelocity)/interWheelDistance)
	position=simGetObjectPosition(robotHandle,sim_handle_parent)
	orientation=simGetObjectOrientation(robotHandle,sim_handle_parent)
	xDir={math.cos(orientation[3]),math.sin(orientation[3]),0.0}
	position[1]=position[1]+xDir[1]*linVar
	position[2]=position[2]+xDir[2]*linVar
	orientation[3]=orientation[3]+rotVar
	simSetObjectPosition(robotHandle,sim_handle_parent,position)
	simSetObjectOrientation(robotHandle,sim_handle_parent,orientation)
	-- Now make the wheels turn:
	jointP=simGetJointPosition(leftJointHandle)
	jointP=jointP+leftVelocity*dt/wheelRadius
	simSetJointPosition(leftJointHandle,jointP)
	jointP=simGetJointPosition(rightJointHandle)
	jointP=jointP+rightVelocity*dt/wheelRadius
	simSetJointPosition(rightJointHandle,jointP)
	-- Now make the proximity sensors move:
	if (sensorRotationVelocity>=0) then
		sensorRotationVelocity=navigationParams[3]
	else
		sensorRotationVelocity=-navigationParams[3]
	end
	rotPos=simGetJointPosition(sensorJointHandle) 
	rotPos=rotPos+sensorRotationVelocity*dt
	if (rotPos<-math.pi/2) then
		rotPos=-math.pi-rotPos
		sensorRotationVelocity=math.abs(sensorRotationVelocity)
	end
	if (rotPos>0) then
		rotPos=-rotPos
		sensorRotationVelocity=-math.abs(sensorRotationVelocity)
	end
	simSetJointPosition(sensorJointHandle,rotPos)
	
	travelledDistance=travelledDistance+linVar
	simSetScriptSimulationParameter(sim_handle_self,'travelledDistance',travelledDistance)
	
	score=tonumber(simGetScriptSimulationParameter(sim_handle_self,'score'))+linVar
	simSetScriptSimulationParameter(sim_handle_self,'score',score)
	
	-- Are we colliding? if yes we kill ourselves!
	if (simHandleCollision(collisionHandle)>0) then
		removeRobot=true
		simAddStatusbarMessage("Robot collided!")
		simSetScriptSimulationParameter(sim_handle_self,'isFinished',"true")
	end
	
	-- Now display info in the UI:
	simSetUIButtonLabel(userInterfaceHandle,ui_timePassedH,simGetSimulationTime()-startTime)
	simSetUIButtonLabel(userInterfaceHandle,ui_score,score)
	simSetUIButtonLabel(userInterfaceHandle,ui_maxSpeed,navigationParams[1])
	simSetUIButtonLabel(userInterfaceHandle,ui_minSpeed,navigationParams[2])
	simSetUIButtonLabel(userInterfaceHandle,ui_sweepSpeed,navigationParams[3])
	simSetUIButtonLabel(userInterfaceHandle,ui_detectionPersistence,navigationParams[4])
	simSetUIButtonLabel(userInterfaceHandle,ui_detectionDistance,navigationParams[5])

	--if (removeRobot) then
	--	simSetIntegerSignal("lastRobotRemovalTime",simGetSimulationTime())
	--	r=simGetObjectAssociatedWithScript(sim_handle_self)
	--	simRemoveModel(r)
	--end

end 
