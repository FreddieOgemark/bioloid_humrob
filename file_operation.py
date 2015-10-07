class FileOperations:

    def __init__(self, fileName):
        
        self.lines = []
        self.parameterValues = []
        with open(fileName) as f:
            self.lines = self.lines + f.readlines()


    def showContent(self):
        
        for i in range(len(self.lines)):
            values = self.lines[i].replace("\n","").split(',')
            for j in range(len(values)):
                if values[j].replace(" ","") != "":
                    print(values[j])
                    self.parameterValues.append(float(values[j]))

        return self.parameterValues


#f = FileOperations('genomeData/2015-10-02_15-51-12_bestGenome.csv')
#content = f.showContent()
#print(content)
