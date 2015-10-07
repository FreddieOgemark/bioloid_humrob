<<<<<<< HEAD:file_Operation.py
import os

class fileOperations:
=======
class FileOperations:
>>>>>>> origin/master:file_operation.py

    def __init__(self, folderName):
        fileName = self.getLastGeneratedFile(folderName)
        #print fileName
        self.lines = []
        self.parameterValues = []
        with open(fileName) as f:
            self.lines = self.lines + f.readlines()


    def getContent(self):
        
        for i in range(len(self.lines)):
            values = self.lines[i].replace("\n","").split(',')
            for j in range(len(values)):
                if values[j].replace(" ","") != "":
                    #print(values[j])
                    self.parameterValues.append(float(values[j]))

        return self.parameterValues

    def getLastGeneratedFile(self, folderName):
        txtFilesInDir = []
        if os.path.isdir(folderName):
            for root, dirs, files in os.walk(folderName):
                for name in files:
                    if name.endswith(("csv")):
                        #print os.path.join(root, name)
                        txtFilesInDir.append(name)
                        #print name

<<<<<<< HEAD:file_Operation.py
        maxDate = ""
        for fName in txtFilesInDir:
            #print fName[0:19]
            if fName[0:19] >= maxDate:
                #print "True"
                maxDate = fName[0:19]
                lastFile = fName
                
        #print lastFile
        return lastFile
                        

#f = fileOperations("D:\Alireza_UniDocuments\Chalmers University\Semester 3\Humanoid Robotics\Git\TIF160_Bioloid")
=======
#f = FileOperations('genomeData/2015-10-02_15-51-12_bestGenome.csv')
>>>>>>> origin/master:file_operation.py
#content = f.showContent()
#print(content)

#f.getContent()
