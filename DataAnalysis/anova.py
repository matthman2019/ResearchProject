import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from statistics import mean, stdev
import scipy.stats as stats

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

languageToAlgToData : dict[str, dict[str, list[float]]] = {}
graphHeight = 100
def loadData(filename : Path, language : str ):
    global graphHeight, languageToAlgToData
    loadedDictionary = openFile(filename)
    languageToAlgToData[language] = {}
    for key, value in loadedDictionary.items():
        print(key)
        languageToAlgToData[language][key] = value


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
    
    fileList : list[Path] = []
    for file in Path(__file__).parent.iterdir():
        if not file.is_file():
            continue
        if file.suffix == ".txt":
            fileList.append(file)
    
    for file in fileList:
        languageName = file.name.removesuffix("Output.txt")
        loadData(file, languageName)

    print(languageToAlgToData)

print(languageToAlgToData)



