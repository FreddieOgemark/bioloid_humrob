import random

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

    def __init__(self, functionClass, nrIndividualsPerGeneration):
        print("Initializing genetic algorithm")

        self.functionClass = functionClass
        self.nrIndividualsPerGeneration = nrIndividualsPerGeneration

        for i in range(self.nrIndividualsPerGeneration):
            self.currentFitness.append(0)
            self.currentGenomes.append(self.functionClass.initializeGenome())
        self.pMut = 1/len(self.currentGenomes[0])
        print("pMut set to " + str(self.pMut))
        print("Initialization done")

    def findBestInGenerationIndex(self, populationFitness):
        bestInGenerationIndex = 1
        for i in range(2, self.nrIndividualsPerGeneration):
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
        print("Genome: " + self.genomeToString(self.currentGenomes[bestInGenerationIndex]))
        newGenomes.append(self.currentGenomes[bestInGenerationIndex])
        if (self.currentFitness[bestInGenerationIndex] > self.bestFitness):
            # save the globally best genome (over all time)
            self.bestFitness = self.currentFitness[bestInGenerationIndex]
            self.bestGenome = self.currentGenomes[bestInGenerationIndex]

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

