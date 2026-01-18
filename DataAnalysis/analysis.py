import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from statistics import mean

def openFile(filePath : Path) -> dict:
    sortReading = ''
    returnDict = {}
    with open(filePath, 'r') as file:
        for line in file:
            line = line.rstrip("\n")

            if "=" in line:
                line = line.strip("=")
                sortReading = line
                if not sortReading in returnDict.keys():
                    returnDict[sortReading] = []
                continue

            try:
                line = int(line)
            except ValueError:
                continue

            returnDict[sortReading].append(line)

    return returnDict

if __name__ == "__main__":
    fileDict = openFile(Path("/home/matthman2019/ResearchProject/DataAnalysis/PythonOutput.txt"))
    plt.bar(list(fileDict.keys()), list(map(mean, fileDict.values())))
    plt.show()