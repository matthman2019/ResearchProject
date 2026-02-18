import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from statistics import mean, stdev

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

graphHeight = 100
def loadData(graph, filename : Path, language : str, color : str):
    global graphHeight
    loadedDictionary = openFile(filename)
    meanList = list(map(mean, loadedDictionary.values()))
    stdDevList = list(map(stdev, loadedDictionary.values()))
    sampleSize = len(loadedDictionary["Bubble"])
    stdErrList = list(map(lambda x: x / sampleSize, stdDevList))
    graph.bar(list(loadedDictionary.keys()), meanList, yerr=stdErrList, color=color)
    graph.set_title(f"{language} Output")
    graph.set_ylim(0, graphHeight)
    graph.tick_params(axis='both', labelsize=6)
    print(f"{language}: {meanList}")

colorDict = {
    "Python" : "blue",
    "PyPy" : "mediumblue",
    "Javascript" : "red",
    "Lua" : "skyblue",
    "LuaJIT" : "deepskyblue",
    "C++" : "green",
    "Java" : "orange",
    "Rust" : "brown",
    "Go" : "teal",
    "Perl" : "khaki"
}

if __name__ == "__main__":
    
    fig, ((ax1, ax2, ax3, ax4, ax5), (ax6, ax7, ax8, ax9, ax10)) = plt.subplots(2, 5)
    axList = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10]
    fileList : list[Path] = []
    for file in Path(__file__).parent.iterdir():
        if not file.is_file():
            continue
        if file.suffix == ".txt":
            fileList.append(file)
    
    for file, graph in zip(fileList, axList):
        languageName = file.name.removesuffix("Output.txt")
        loadData(graph, file, languageName, colorDict[languageName])

    plt.show()
