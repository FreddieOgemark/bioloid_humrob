#from AbstractFunctionClass import AbstractFunctionClass

class GenAlg:

    nrIndividualsPerGeneration = 20
    pTour = 0.75
    pCross = 0.5
    pMut = 0.1

    functionClass = None
    robotNameID = "unnamed"
    generationNr = 1
    individualNr = 1

    currentFitness = []
    currentGenomes = []

    bestFitness = 0
    bestGenome = []

    def __init__(self, robotNameID, functionClass):
        print("Initializing genetic algorithm")
        self.robotNameID = robotNameID
        self.functionClass = functionClass

        for i in range(self.nrIndividualsPerGeneration):
            self.currentFitness.append(0)
            self.currentGenomes.append(functionClass.initializeGenome())
        print("Initialization done")

    def onFrame(self):
        self.variable = 42
        return "whatisthis?"



