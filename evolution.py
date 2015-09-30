import cpg.simulation
import cpg.bioloid_network
import natsel.AbstractFunctionClass
import natsel.GenAlg

import random

class Individual(natsel.AbstractFunctionClass.AbstractFunctionClass):
    def initializeGenome(self):
        # Should return a genome, that is, an array/list with floating values
        genome = []
        ranges = self.getGenomeRange()
        for i in range(len(ranges)):
            genome.append(ranges[i][0] + random.random()*(ranges[i][1]-ranges[i][0]))
        cpg.bioloid_network.get_random_weights(8,8)
        return genome

    def getGenomeRange(self):
        # Should return a list of [min, max] ranges for each parameter in the genome
        # For example, if parameter 1 in the genome has an allowed range of (-2, 3) 
        # and parameter 2 in the genome has the allowed range (3, 5), then this function
        # should return the list [[-2, 3], [3, 5], ...]
        ranges = []
        for i in range(8*8):
            ranges.append([-1.0, 1.0])
        return ranges

    def getFitness(self, genome):
        # Should calculate the fitness of the specified genome and return it
        return cpg.simulation.evaluate_individual(genome)

print('Starting evolution...')

myInd = Individual()
ga = natsel.GenAlg.GenAlg(myInd, 20)

for generation in range(20):
    ga.runGeneration()

ga.printResults()