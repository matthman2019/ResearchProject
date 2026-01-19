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
                line = line.rstrip(" Sort")
                sortReading = line
                if not sortReading in returnDict.keys():
                    returnDict[sortReading] = []
                continue

            try:
                line = float(line)
            except ValueError:
                continue

            returnDict[sortReading].append(line)

    return returnDict



if __name__ == "__main__":
    pythonDict = openFile(Path("/home/matthman2019/ResearchProject/DataAnalysis/WrongComputer2PythonOutput.txt"))
    javascriptDict = openFile(Path("/home/matthman2019/ResearchProject/DataAnalysis/WrongComputer4JavascriptOutput.txt"))
    luaDict = openFile(Path("/home/matthman2019/ResearchProject/DataAnalysis/WrongComputerLuaOutput.txt"))

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    
    ax1.bar(list(pythonDict.keys()), list(map(mean, pythonDict.values())), color="blue")
    ax1.set_title("Python Output")
    ax1.set_ylim(0, 850)
    ax2.bar(list(javascriptDict.keys()), list(map(mean, javascriptDict.values())), color="red")
    ax2.set_title("Javascript Output")
    ax2.set_ylim(0, 850)
    ax3.bar(list(luaDict.keys()), list(map(mean, luaDict.values())), color="skyblue")
    ax3.set_title("Lua Output")
    ax3.set_ylim(0, 850)

    print(list(map(mean, pythonDict.values())))
    print(list(map(mean, javascriptDict.values())))
    print(list(map(mean, luaDict.values())))
    plt.show()