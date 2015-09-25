
function genomeToString (genome)
	output = "("
	for i=1,genomeSize do
		output = output .. genome[i] .. ", "
	end
	output = string.sub(output, 1, string.len(output)-2)
	output = output .. ")"
	return output
end

function initializeGenome ()
	genome = {}
	genome[1] = -2.5+math.random()*5 -- posX
	genome[2] = -2.5+math.random()*5 -- posY
	genome[3] = math.random()*2*math.pi -- orientation
	return genome
end

function getFitness(genome)
	-- calculate robot's score/fitness
	-- distance from robot's start location
	robotPos = simGetObjectPosition(robotHandle, -1)
	robotGenome = genome
	travelledDist = math.sqrt(math.pow(robotPos[1] - robotGenome[1], 2) + math.pow(robotPos[2] - robotGenome[2], 2))
	return travelledDist
end

function findBestInGenerationIndex()
	bestInGenerationIndex = 1
	for i=2,simGetIntegerSignal('nrIndividualsPerGeneration') do
		-- find best in generation
		if (currentFitness[i] > currentFitness[bestInGenerationIndex]) then
			bestInGenerationIndex = i
		end
	end
	return bestInGenerationIndex
end

function arrayClone(original)
	clone = {}
	for i=1, #original do
		clone[i] = original[i]
	end
	return clone
end

function tournamentSelection(population, fitness)
	winnerGenome = {}
	ind1 = math.random( #population )
	ind2 = math.random( #population )
	if (fitness[ind1] > fitness[ind2]) then
		betterInd = ind1
		worserInd = ind2
	else
		betterInd = ind2
		worserInd = ind1
	end
	if (math.random() < simGetFloatSignal('pTour')) then
		winnerGenome = arrayClone(population[betterInd])
	else
		winnerGenome = arrayClone(population[worserInd])
	end
	return winnerGenome
end

function mutate(genome)
	if (math.random() < simGetFloatSignal('pMut')) then
		-- mutate the start posX
		genome[1] = genome[1] + (math.random()*0.2-0.1)
		
		-- make sure position is valid
		if (genome[1] < -2.5) then
			genome[1] = -2.5
		elseif (genome[1] > 2.5) then
			genome[1] = 2.5
		end
	end
	if (math.random() < simGetFloatSignal('pMut')) then
		-- mutate the start posY
		genome[2] = genome[2] + (math.random()*0.2-0.1)
		
		-- make sure position is valid
		if (genome[2] < -2.5) then
			genome[2] = -2.5
		elseif (genome[2] > 2.5) then
			genome[2] = 2.5
		end
	end
	if (math.random() < simGetFloatSignal('pMut')) then
		-- mutate the start rotation
		genome[3] = genome[3] + (math.random()*0.8-0.4)
	end
	return genome
end

function initializeRobot(robotHandle, genome)
	startPosX = genome[1]
	startPosY = genome[2]
	startRot = genome[3]
	simSetObjectPosition(robotHandle,sim_handle_parent,{startPosX,startPosY,0})
	simSetObjectOrientation(robotHandle,sim_handle_parent,{0,0,startRot})
end

-- DO NOT WRITE CODE OUTSIDE OF THE if-then-end SECTIONS BELOW!! (unless the code is a function definition)

if (sim_call_type==sim_childscriptcall_initialization) then

	-- Initialization of evolutionary algorithm
	simAddStatusbarMessage("Initializing evolutionary algorithm")

	robotNameID = "dr12_robot_"
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

	-- genomes stored in matrix of size (nrIndividuals, genomeSize)
	currentGenomes = {}          -- create the matrix
    for i=1,simGetIntegerSignal('nrIndividualsPerGeneration') do
		currentGenomes[i] = initializeGenome()
    end
	genomeSize = #currentGenomes[1] -- length of first genome
	
	-- best fitness is just a number
	bestFitness = 0
	-- best genome is an array
	bestGenome = {}
	
	simAddStatusbarMessage("EA initialized")
end


if (sim_call_type==sim_childscriptcall_actuation) then

	-- Called every frame (or something like that)
	robotScriptHandle = simGetScriptHandle(robotNameID)
	robotHandle = simGetObjectHandle(robotNameID)
	robotIsFinished = simGetScriptSimulationParameter(robotScriptHandle, "isFinished")
	if (robotIsFinished == true) then
		simAddStatusbarMessage("Robot is finished")

		-- get robot's score/fitness
		currentFitness[individualNr] = getFitness(currentGenomes[individualNr])
		simAddStatusbarMessage("Fitness: " .. currentFitness[individualNr])

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
		bestInGenerationIndex = findBestInGenerationIndex()
		simAddStatusbarMessage("Index of best in generation: " .. tostring(bestInGenerationIndex))
		simAddStatusbarMessage("Genome: " .. genomeToString(currentGenomes[bestInGenerationIndex]))
		newGenomes[1] = currentGenomes[bestInGenerationIndex]
		if (currentFitness[bestInGenerationIndex] > bestFitness) then
			-- Save the globally best genome
			bestFitness = currentFitness[bestInGenerationIndex]
			bestGenome = currentGenomes[bestInGenerationIndex]
		end

		for i=2,simGetIntegerSignal('nrIndividualsPerGeneration') do
			newGenomes[i] = {}     -- create a new row
			
			-- do tournament selection
			winnerGenome = tournamentSelection(currentGenomes, currentFitness)
			newGenomes[i] = winnerGenome

			-- MUTATION
			newGenomes[i] = mutate(newGenomes[i])
		end

		currentGenomes = newGenomes
		firstGenome = currentGenomes[1]
		simAddStatusbarMessage("Genome: " .. genomeToString(firstGenome))

		-- increase generation count and reset individual count
		generationNr = generationNr+1
		individualNr = 1
	end

	if (robotIsFinished == true) then
		-- must now initialise the new individual
		initializeRobot(robotHandle, currentGenomes[individualNr])
		simSetScriptSimulationParameter(robotScriptHandle, "isFinished", "false")

		simAddStatusbarMessage("")
		simAddStatusbarMessage("Robot was reset")
		simAddStatusbarMessage("Generation " .. tostring(generationNr) .. ", individual " .. tostring(individualNr))
	end
end


if (sim_call_type==sim_childscriptcall_sensing) then

	-- Put your main SENSING code here

end


if (sim_call_type==sim_childscriptcall_cleanup) then

	simAddStatusbarMessage("")
	simAddStatusbarMessage("CLEANUP")
	-- Print info or save to file or something
	simAddStatusbarMessage("Best genome during the whole simulation:")
	simAddStatusbarMessage(genomeToString(bestGenome))
	simAddStatusbarMessage("Fitness of best genome: " .. tostring(bestFitness))
end