from AbstractFunctionClass import AbstractFunctionClass
import random
import math

class TestFunctionClass(AbstractFunctionClass):

    def initializeGenome(self):
        # Should return a genome, that is, an array/list with floating values
        genome = []
        ranges = self.getGenomeRange()
        for i in range(len(ranges)):
            genome.append(ranges[i][0] + random.random()*(ranges[i][1]-ranges[i][0]))
        return genome

    def getGenomeRange(self):
        # Should return a list of [min, max] ranges for each parameter in the genome
        # For example, if parameter 1 in the genome has an allowed range of (-2, 3) 
        # and parameter 2 in the genome has the allowed range (3, 5), then this function
        # should return the list [[-2, 3], [3, 5], ...]
        ranges = []
        ranges.append([-2.5, 2.5]) # posX
        ranges.append([-2.5, 2.5]) # posY
        ranges.append([0, 2*math.pi]) # orientation
        ranges.append([0.6, 1.2]) # max speed
        ranges.append([0.1, 0.3]) # min speed
        ranges.append([5*math.pi/180, 90*math.pi/180]) # sweep speed
        ranges.append([-0.1, 2]) # detection persistence
        ranges.append([0.1, 0.7]) # detection distance
        return ranges

    def getFitness(self, genome):
        # Should calculate the fitness of the specified genome and return it
        raise NotImplementedError()