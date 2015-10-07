from cpg import simulation, bioloid_network
from natsel import abstract_function_class, gen_alg

import random
import time
import sys

class Individual(abstract_function_class.AbstractFunctionClass):
    def initializeGenome(self):
        # Should return a genome, that is, an array/list with floating values
        genome = []
        ranges = self.getGenomeRange()
        for i in range(len(ranges)):
            genome.append(ranges[i][0] + random.random()*(ranges[i][1]-ranges[i][0]))
        bioloid_network.get_random_weights(8,8)
        return genome

    def getGenomeRange(self):
        # Should return a list of [min, max] ranges for each parameter in the genome
        # For example, if parameter 1 in the genome has an allowed range of (-2, 3) 
        # and parameter 2 in the genome has the allowed range (3, 5), then this function
        # should return the list [[-2, 3], [3, 5], ...]
        ranges = []
        for i in range(8*8):
            ranges.append([-1.5, 1.5])
        return ranges

    def getFitness(self, genome):
        # Should calculate the fitness of the specified genome and return it
        return simulation.evaluate_individual(genome)

initPopFilename = None
if (len(sys.argv) == 2):
    # assuming the second parameter is name of file containing the initial population
    initPopFilename = sys.argv[1]
    print("File containing initial population:", initPopFilename)

simulation.connect_to_vrep()

print('Starting evolution...')

start_time = time.time()

populationSize = 10
generations = 5

myInd = Individual()
ga = gen_alg.GenAlg(myInd, populationSize, initPopFilename)

for generation in range(generations):
    ga.runGeneration()
    print("\n--- GA has currently run for " + str(time.time()-start_time) + " seconds ---")

ga.printResults()

simulation.disconnect_from_vrep()

print("\n--- Total execution time: " + str(time.time()-start_time) + " seconds ---")