from scipy import stats
from pathlib import Path

# this doesn't actually do a posthoc test
# this does other operations to analyze the data

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

fileList = []
for file in Path(__file__).parent.iterdir():
    if not file.is_file():
        continue
    if file.suffix == ".txt":
        fileList.append(file)

languageToData : dict[str, dict[str, list[float]]]= {}
for file in fileList:
    languageName = file.name.removesuffix("Output.txt")
    languageToData[languageName] = openFile(file)

sortSpeedList = ["Quick", "Insertion", "Merge", "Radix", "Bubble"]
languageSpeedList = ["C++", "Java", "Rust", "Go", "LuaJIT", "PyPy", "Lua", "Javascript", "Perl", "Python"]

def getData(language : str, sort : str):
    return languageToData[language][sort]

def testLanguage(sort : str):
    with open("ttest.out", "a") as file:
        for index, language in enumerate(languageSpeedList):
            if index == len(languageSpeedList) - 1:
                break
            
            slowerLanguage = languageSpeedList[index + 1]
            result = stats.ttest_rel(getData(language, sort), getData(slowerLanguage, sort), alternative="less")
            file.write(f"{sort},{language},{slowerLanguage},{result.statistic},{result.pvalue}\n")

def testSort(language : str):
    with open("ttest.out", "a") as file:
        for index, sort in enumerate(sortSpeedList):
            if index == len(sortSpeedList) - 1:
                break
            
            slowerSort = sortSpeedList[index + 1]
            result = stats.ttest_rel(getData(language, sort), getData(language, slowerSort), alternative="less")
            file.write(f"{language},{sort},{slowerSort},{result.statistic},{result.pvalue}\n")

  
def main():
    open("ttest.txt", "w").close() # I love this line
    for sort in sortSpeedList:
        testLanguage(sort)
    for language in languageSpeedList:
        testSort(language)


if __name__ == "__main__":
    main()
