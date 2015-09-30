import random

class GenAlg:

    nrIndividualsPerGeneration = 10 # default
    pTour = 0.75
    pCross = 0.5
    pMut = 0.1

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
            self.currentGenomes.append(functionClass.initializeGenome())
        print("Initialization done")

    def findBestInGenerationIndex(self, populationFitness):
        bestInGenerationIndex = 1
        for i in range(2, nrIndividualsPerGeneration):
            # find best in generation
            if (populationFitness[i] > populationFitness[bestInGenerationIndex]):
                bestInGenerationIndex = i

        return bestInGenerationIndex

    def genomeToString(self, genome):
        output = "("
        for i in range(len(genome)):
            output = output + genome[i] + ", "
        output = output[:-2] # remove final ", "
        output = output + ")"
        return output

    def clampValue(value, min, max):
        if (calue < min):
            value = min
        elif (value > max):
            value = max
        return value

    def tournamentSelection(population, fitness, probTour):
        winnerGenome = []
        ind1 = random.randint(0, len(population))
        ind2 = random.randint(0, len(population))
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

    def crossover(genome1, genome2):
        crossoverIndex = random.randint(0, len(genome1))
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

    def mutate(genome, probMut):
        ranges = functionClass.getGenomeRange()
        # for each gene in the genome
        for i in range(len(ranges)):
            if (random.random() < probMut):
                change = (ranges[i][1] - ranges[i][0])*0.1 # max 10 % of total range interval
                # mutate
                genome[i] = genome[i] + (random.random()*change - change/2)
                # make sure values is within valid ranges
                genome[i] = self.clampValue(genome[i], ranges[i][0], ranges[i][1])

        return genome

    def runGeneration(self):
        for i in range(nrIndividualsPerGeneration):
            print("Generation " + (generationNr+1) + ", individual " + (i+1))

            # get robot's score/fitness (by simulating it)
            currentFitness[i] = functionClass.getFitness(currentGenomes[i])
            print("Robot is finished")
            print("Fitness: " + currentFitness[i])

            print("")

        # we are now done with a generation
        # create a new generation from the previous one
        newGenomes = []

        # ELITISM HERE
        bestInGenerationIndex = self.findBestInGenerationIndex(currentFitness)
        print("Index of best in generation: " + bestInGenerationIndex)
        print("Genome: " + self.genomeToString(currentGenomes[bestInGenerationIndex]))
        newGenomes.append(currentGenomes[bestInGenerationIndex])
        if (currentFitness[bestInGenerationIndex] > bestFitness):
            # save the globally best genome (over all time)
            bestFitness = currentFitness[bestInGenerationIndex]
            bestGenome = currentGenomes[bestInGenerationIndex]

        for i in range(2, nrIndividualsPerGeneration):
            newGenomes.append([]) # create new position for genome
            # TOURNAMENT SELECTION
            winnerGenome = self.tournamentSelection(currentGenomes, currentFitness, pTour)
            newGenomes[i] = winnerGenome

            # CROSSOVER (this version only saves one of the "crossovered" individuals)
            if (random.random() < pCross):
                otherGenome = self.tournamentSelection(currentGenomes, currentFitness, pTour)
                newGenomes[i] = self.crossover(newGenomes[i], otherGenome)

            # MUTATION
            newGenomes[i] = self.mutate(newGenomes[i], pMut)

        currentGenomes = newGenomes
        # prints the best genome (assuiming elitism is activated so the best has index 0)
        print("Best genome this generation: " + self.genomeToString(currentGenomes[0]))

        # increase generation count
        generationNr += 1

        print("Generation " + generationNr + " done")
        print("")


    def onCleanup(self):
        print("")
        print("Time for cleanup")
        # Print info or save to file or something
        print("Best genome during the whole simulation:")
        print(self.genomeToString(bestGenome))
        print("Fitness of best genome: " + bestFitness)

