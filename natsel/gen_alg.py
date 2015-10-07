import random
import datetime
import os

def clampValue(value, min, max):
    if (value < min):
        value = min
    elif (value > max):
        value = max
    return value

class GenAlg:

    nrIndividualsPerGeneration = 10 # default
    pTour = 0.75
    pCross = 0.5
    pMut = 0.1 # currently overwritten in constructor to 1/genomeLength

    functionClass = None
    generationNr = 0 # when displayed, add 1 (must start from 0 because Python index)

    currentFitness = []
    currentGenomes = []

    bestFitness = 0
    bestGenome = []

    def __init__(self, functionClass, nrIndividualsPerGeneration, initPopFilename):
        print("Initializing genetic algorithm")

        self.functionClass = functionClass
        self.nrIndividualsPerGeneration = nrIndividualsPerGeneration
        genomeLength = len(self.functionClass.getGenomeRange())
        self.pMut = 1/genomeLength
        print("pMut set to " + str(self.pMut))

        successReadingInitPop = False
        if ((not (initPopFilename is None)) and os.path.exists(initPopFilename)):
            # primarily use the initial population
            initPop = self.readInitialPopFile(initPopFilename, genomeLength)
            if not (initPop is None):
                # managed to load an initial population, there are now three cases
                # initPop.length < nrIndividualsPerGeneration: fill up remainder with mutated
                if (len(initPop) < nrIndividualsPerGeneration):
                    for i in range(nrIndividualsPerGeneration):
                        if (i < len(initPop)):
                            self.currentGenomes.append(initPop[i])
                        else:
                            rndIndex = random.randint(0, len(initPop)-1)
                            self.currentGenomes.append(self.mutate(initPop[rndIndex], self.pMut))
                # initPop.length > nrIndividualsPerGeneration: only pick first ones
                else:# (len(initPop) > nrIndividualsPerGeneration):
                    for i in range(nrIndividualsPerGeneration):
                        self.currentGenomes.append(initPop[i])
                # initPop.length == nrIndividualsPerGeneration: pick it as is
                    # same as the previous one
                successReadingInitPop = True

        # if we failed to read init pop, initialize randomly instead
        if not successReadingInitPop:
            print("Failed reading init pop file, initializing from scratch instead")
            # create entirely new population
            for i in range(self.nrIndividualsPerGeneration):
                self.currentGenomes.append(self.functionClass.initializeGenome())
        # init fitness
        for i in range(self.nrIndividualsPerGeneration):
                self.currentFitness.append(0)
        print("Initialization done")

    def readInitialPopFile(self, initPopFilename, expectedGenomeLength):
        # can assume that initPopFilename is not None and the file exists
        f = open(initPopFilename)
        population = []
        allLines = list(f)
        for k in range(len(allLines)):
            # each line is a genome
            genome = []
            line = allLines[k]
            valueStrings = line.split(",")
            if (len(valueStrings) != expectedGenomeLength):
                # Can't read genome since it has wrong length!
                print("ERROR: Genome in initial population had length", len(valueStrings), "while the expected genome length was", expectedGenomeLength)
                return None
            for i in range(len(valueStrings)):
                genome.append(float(valueStrings[i]))
            population.append(genome)
        return population


    def findBestInGenerationIndex(self, populationFitness):
        bestInGenerationIndex = 0
        for i in range(1, self.nrIndividualsPerGeneration):
            # find best in generation
            if (populationFitness[i] > populationFitness[bestInGenerationIndex]):
                bestInGenerationIndex = i

        return bestInGenerationIndex

    def genomeToString(self, genome):
        output = "("
        for i in range(len(genome)):
            output = output + str(genome[i]) + ", "
        output = output[:-2] # remove final ", "
        output = output + ")"
        return output

    def tournamentSelection(self, population, fitness, probTour):
        winnerGenome = []
        ind1 = random.randint(0, len(population)-1)
        ind2 = random.randint(0, len(population)-1)
        if (fitness[ind1] > fitness[ind2]):
            betterInd = ind1
            worserInd = ind2
        else:
            betterInd = ind2
            worserInd = ind1

        if (random.random() < probTour):
            winnerGenome = list(population[betterInd])
        else:
            winnerGenome = list(population[worserInd])
        return winnerGenome

    def crossover(self, genome1, genome2):
        crossoverIndex = random.randint(0, len(genome1)-1)
        for i in range(crossoverIndex, len(genome1)):
            # assuming genomes have same length
            tmp = genome1[i]
            genome1[i] = genome2[i]
            genome2[i] = tmp

        # to avoid bias, must switch between which is returned as long as only returning one genome
        if (random.random() < 0.5):
            return genome1
        else:
            return genome2

    def mutate(self, genome, probMut):
        ranges = self.functionClass.getGenomeRange()
        # for each gene in the genome
        for i in range(len(ranges)):
            if (random.random() < probMut):
                change = (ranges[i][1] - ranges[i][0])*0.1 # max 10 % of total range interval
                # mutate
                if (random.random() < 0.7):
                    # creep mutation
                    genome[i] = genome[i] + (random.random()*change - change/2)
                else:
                    # random mutation
                    genome[i] = ranges[i][0] + random.random()*(ranges[i][1]-ranges[i][0])
                # make sure values is within valid ranges
                genome[i] = clampValue(genome[i], ranges[i][0], ranges[i][1])

        return genome

    def runGeneration(self):
        for i in range(self.nrIndividualsPerGeneration):
            print("Generation " + str(self.generationNr+1) + ", individual " + str(i+1))

            # get robot's score/fitness (by simulating it)
            self.currentFitness[i] = self.functionClass.getFitness(self.currentGenomes[i])
            print("Robot is finished")
            print("Fitness: " + str(self.currentFitness[i]))

            print("")

        # we are now done with a generation
        # create a new generation from the previous one
        newGenomes = []

        # ELITISM HERE
        bestInGenerationIndex = self.findBestInGenerationIndex(self.currentFitness)
        print("Index of best in generation: " + str(bestInGenerationIndex))
        #print("Genome: " + self.genomeToString(self.currentGenomes[bestInGenerationIndex]))
        newGenomes.append(self.currentGenomes[bestInGenerationIndex])
        if (self.currentFitness[bestInGenerationIndex] > self.bestFitness):
            # save the globally best genome (over all time)
            self.bestFitness = self.currentFitness[bestInGenerationIndex]
            self.bestGenome = self.currentGenomes[bestInGenerationIndex]
            print("*** New best fitness found! ", self.bestFitness)

        for i in range(1, self.nrIndividualsPerGeneration):
            newGenomes.append([]) # create new position for genome
            # TOURNAMENT SELECTION
            winnerGenome = self.tournamentSelection(self.currentGenomes, self.currentFitness, self.pTour)
            newGenomes[i] = winnerGenome

            # CROSSOVER (this version only saves one of the "crossovered" individuals)
            if (random.random() < self.pCross):
                otherGenome = self.tournamentSelection(self.currentGenomes, self.currentFitness, self.pTour)
                newGenomes[i] = self.crossover(newGenomes[i], otherGenome)

            # MUTATION
            newGenomes[i] = self.mutate(newGenomes[i], self.pMut)

        self.currentGenomes = newGenomes
        # prints the best genome (assuiming elitism is activated so the best has index 0)
        #print("Best genome this generation: " + self.genomeToString(self.currentGenomes[0]))
        print("Current best genome fitness: " + str(self.bestFitness))

        # increase generation count
        self.generationNr += 1

        print("Generation " + str(self.generationNr) + " done")
        print("")


    def printResults(self):
        print("")
        print("Time for cleanup")
        # Print info or save to file or something
        print("Best genome during the whole simulation:")
        print(self.genomeToString(self.bestGenome))
        print("Fitness of best genome: " + str(self.bestFitness))


        print("Writing best genome and current population to file")
        dataFolder = "genomeData/"
        if not os.path.exists(dataFolder):
            os.makedirs(dataFolder)
        timestamp = datetime.datetime.today()
        timestampString = timestamp.strftime('%Y-%m-%d_%H-%M-%S')

        genomeFileName = "bestGenome"
        genomeFile = open(dataFolder + timestampString + "_" + genomeFileName + ".csv", 'w')
        line = ""
        for i in range(len(self.bestGenome)):
            line = line + str(self.bestGenome[i]) + ","
        line = line[:-1] + "\n"
        genomeFile.write(line)
        genomeFile.close()
        print("Best genome should be written to file")

        populationFileName = "population"
        populationFile = open(dataFolder + timestampString + "_" + populationFileName + ".csv", 'w')
        outputText = ""
        for k in range(len(self.currentGenomes)):
            line = ""
            for i in range(len(self.currentGenomes[k])):
                line = line + str(self.currentGenomes[k][i]) + ","
            line = line[:-1] + "\n"
            outputText = outputText + line
        populationFile.write(outputText)
        populationFile.close()
        print("Population should be written to file")

