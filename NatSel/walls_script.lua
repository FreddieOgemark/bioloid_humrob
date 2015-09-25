-- DO NOT WRITE CODE OUTSIDE OF THE if-then-end SECTIONS BELOW!! (unless the code is a function definition)

if (sim_call_type==sim_childscriptcall_initialization) then

	-- Put some initialization code here
	simAddStatusbarMessage("Setting values")
	generationNr = 1
	individualNr = 1
	simSetIntegerSignal('nrIndividualsPerGeneration',20)
	simSetFloatSignal('pTour',0.75)
	simSetFloatSignal('pMut',0.05)

	-- fitness stored in an array of length nrIndividuals
	currentFitness = {}    -- new array
    for i=1, simGetIntegerSignal('nrIndividualsPerGeneration') do
		currentFitness[i] = 0
    end

	-- genomes stored in matrix of size (nrIndividuals, ...)
	genomeSize = 3 -- posx, posy, rotation
	currentGenomes = {}          -- create the matrix
    for i=1,simGetIntegerSignal('nrIndividualsPerGeneration') do
		currentGenomes[i] = {}     -- create a new row
		currentGenomes[i][1] = -2.5+math.random()*5
		currentGenomes[i][2] = -2.5+math.random()*5
		currentGenomes[i][3] = math.random()*2*math.pi
    end
	
	-- best fitness is just a number
	bestFitness = 0
	-- best genome is an array
	bestGenome = {}
	
	simAddStatusbarMessage("Values are set")

end


if (sim_call_type==sim_childscriptcall_actuation) then

	-- Put your main ACTUATION code here
	

	-- actual code :D
	robotScriptHandle = simGetScriptHandle("dr12_robot_")
	robotHandle = simGetObjectHandle("dr12_robot_")
	robotIsFinished = simGetScriptSimulationParameter(robotScriptHandle, "isFinished")
	if (robotIsFinished == true) then
		simAddStatusbarMessage("Robot is finished")

		-- CHANGE: calculate and save robot's score/fitness
		-- distance from robot's start location
		robotPos = simGetObjectPosition(robotHandle, -1)
		robotGenome = currentGenomes[individualNr]
		travelledDist = math.sqrt(math.pow(robotPos[1] - robotGenome[1], 2) + math.pow(robotPos[2] - robotGenome[2], 2))
		simAddStatusbarMessage("Distance travelled")
		simAddStatusbarMessage(tostring(travelledDist))
		currentFitness[individualNr] = travelledDist
		

		-- increase individual count
		individualNr = individualNr+1
	else
		-- simAddStatusbarMessage("Robot is still running")
		-- don't need to do anything, just let simulator run
	end

	if (individualNr > simGetIntegerSignal("nrIndividualsPerGeneration")) then
		-- we are now done with a generation

		-- create new generation from the previous one
		newGenomes = {}
		-- ELITISM
		bestInGenerationIndex = 1
		for i=2,simGetIntegerSignal('nrIndividualsPerGeneration') do
			-- find best in generation
			if (currentFitness[i] > currentFitness[bestInGenerationIndex]) then
				bestInGenerationIndex = i
			end
		end
		bestInGenGenome = currentGenomes[bestInGenerationIndex]
		simAddStatusbarMessage("Index of best in generation: " .. tostring(bestInGenerationIndex))
		simAddStatusbarMessage("Genome: " .. genomeToString(bestInGenGenome))
		newGenomes[1] = currentGenomes[bestInGenerationIndex]
		if (currentFitness[bestInGenerationIndex] > bestFitness) then
			-- Save the globally best genome
			bestFitness = currentFitness[bestInGenerationIndex]
			bestGenome = currentGenomes[bestInGenerationIndex]
		end
		for i=2,simGetIntegerSignal('nrIndividualsPerGeneration') do
			newGenomes[i] = {}     -- create a new row
			-- pick two individuals and to tournament selection
			ind1 = math.random( #currentGenomes )
			ind2 = math.random( #currentGenomes )
			if (currentFitness[ind1] > currentFitness[ind2]) then
				betterInd = ind1
				worserInd = ind2
			else
				betterInd = ind2
				worserInd = ind1
			end
			if (math.random() < simGetFloatSignal('pTour')) then
				-- pick best one
				for j=1,genomeSize do
					newGenomes[i][j] = currentGenomes[betterInd][j]
				end
				--newGenomes[i] = currentGenomes[betterInd]
			else
				-- pick worse one
				for j=1,genomeSize do
					newGenomes[i][j] = currentGenomes[betterInd][j]
				end
				--newGenomes[i] = currentGenomes[worserInd]
			end

			-- MUTATION
			if (math.random() < simGetFloatSignal('pMut')) then
				-- mutate the start posX
				newGenomes[i][1] = newGenomes[i][1] + (math.random()*0.2-0.1)
				
				-- make sure position is valid
				if (newGenomes[i][1] < -2.5) then
					newGenomes[i][1] = -2.5
				elseif (newGenomes[i][1] > 2.5) then
					newGenomes[i][1] = 2.5
				end
			end
			if (math.random() < simGetFloatSignal('pMut')) then
				-- mutate the start posY
				newGenomes[i][2] = newGenomes[i][2] + (math.random()*0.2-0.1)
				
				-- make sure position is valid
				if (newGenomes[i][2] < -2.5) then
					newGenomes[i][2] = -2.5
				elseif (newGenomes[i][2] > 2.5) then
					newGenomes[i][2] = 2.5
				end
			end
			if (math.random() < simGetFloatSignal('pMut')) then
				-- mutate the start rotation
				newGenomes[i][3] = newGenomes[i][3] + (math.random()*0.8-0.4)
			end

			-- reset fitness
			--currentFitness[i] = 0
		end
		currentGenomes = newGenomes
		firstGenome = currentGenomes[1]
		simAddStatusbarMessage("Genome: " .. genomeToString(firstGenome))

		-- increase generation count and reset individual count
		generationNr = generationNr+1
		individualNr = 1
	end

	if (robotIsFinished == true) then
		-- TODO must now initialise the new individual
		simSetScriptSimulationParameter(robotScriptHandle, "isFinished", "false")

		startPosX = currentGenomes[individualNr][1]
		startPosY = currentGenomes[individualNr][2]
		startRot = currentGenomes[individualNr][3]
		simSetObjectPosition(robotHandle,sim_handle_parent,{startPosX,startPosY,0})
		simSetObjectOrientation(robotHandle,sim_handle_parent,{0,0,startRot})
		simAddStatusbarMessage("")
		simAddStatusbarMessage("Robot was reset")
		simAddStatusbarMessage("Current individual:")
		simAddStatusbarMessage(tostring(individualNr))
		simAddStatusbarMessage("Current generation:")
		simAddStatusbarMessage(tostring(generationNr))
	end
end


if (sim_call_type==sim_childscriptcall_sensing) then

	-- Put your main SENSING code here

end


if (sim_call_type==sim_childscriptcall_cleanup) then

	simAddStatusbarMessage("THIS IS PRINTED ON CLEANUP")

	-- find the best individual

	-- Print info or save to file or something
	simAddStatusbarMessage("Best genome during the whole simulation:")
	simAddStatusbarMessage(genomeToString(bestGenome))
end

function genomeToString (genome)
	output = "("
	for i=1,genomeSize do
		output = output .. genome[i] .. ", "
	end
	output = string.sub(output, 1, string.len(output)-2)
	output = output .. ")"
	return output
end

function incCount (n)
	n = n or 1
	count = count + n
end