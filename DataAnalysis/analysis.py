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

graphHeight = 10
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

    print(f"{language}: {stdErrList}")

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

    '''
    pythonDict = openFile(Path("PythonOutput2.txt"))
    javascriptDict = openFile(Path("JavascriptOutput2.txt"))
    luaDict = openFile(Path("LuaOutput2.txt"))
    CPPDict = openFile(Path("C++Output2.txt"))
    javaDict = openFile(Path("JavaOutput2.txt"))
    rustDict = openFile(Path("RustOutput2.txt"))
    goDict = openFile(Path("GoOutput2.txt"))
    perlDict = openFile(Path("PerlOutput2.txt"))

    graphHeight = 100
    
    ax1.bar(list(pythonDict.keys()), list(map(mean, pythonDict.values())), color="blue")
    ax1.set_title("Python Output")
    ax1.set_ylim(0, graphHeight)
    ax2.bar(list(javascriptDict.keys()), list(map(mean, javascriptDict.values())), color="red")
    ax2.set_title("Javascript Output")
    ax2.set_ylim(0, graphHeight)
    ax3.bar(list(luaDict.keys()), list(map(mean, luaDict.values())), color="skyblue")
    ax3.set_title("Lua Output")
    ax3.set_ylim(0, graphHeight)
    ax4.bar(list(CPPDict.keys()), list(map(mean, CPPDict.values())), color="green")
    ax4.set_title("C++ Output")
    ax4.set_ylim(0, graphHeight)
    ax5.bar(list(javaDict.keys()), list(map(mean, javaDict.values())), color="orange")
    ax5.set_title("Java Output")
    ax5.set_ylim(0, graphHeight)
    ax6.bar(list(rustDict.keys()), list(map(mean, rustDict.values())), color="brown")
    ax6.set_title("Rust Output")
    ax6.set_ylim(0, graphHeight)
    ax7.bar(list(goDict.keys()), list(map(mean, goDict.values())), color="teal")
    ax7.set_title("Go Output")
    ax7.set_ylim(0, graphHeight)
    ax8.bar(list(perlDict.keys()), list(map(mean, perlDict.values())), color="pink")
    ax8.set_title("Perl Output")
    ax8.set_ylim(0, graphHeight)
    '''
  
    '''


    print(list(map(mean, pythonDict.values())))
    print(list(map(mean, javascriptDict.values())))
    print(list(map(mean, luaDict.values())))
    print(list(map(mean, CPPDict.values())))
    print(list(map(mean, javaDict.values())))
    print(list(map(mean, goDict.values())))
    print(list(map(mean, rustDict.values())))
    print(list(map(mean, perlDict.values())))
    '''

    plt.show()