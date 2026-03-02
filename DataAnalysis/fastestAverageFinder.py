from pathlib import Path
from statistics import mean
from numpy import log10

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


def main():
    # fastest average
    languageScore : list[tuple[str, float]] = []
    for language in languageToData.keys():
        averageList = []
        logAverageList = []
        for data in languageToData[language].values():
            logData = list(map(log10, data))
            averageList.append(mean(data))
            logAverageList.append(mean(logData))
        try:
            languageScore.append((language, mean(averageList), mean(logAverageList)))
        except Exception as e:
            print(f'There was an error with file {language}! {e}')

    print(sorted(languageScore, key=lambda x: x[1]))

    # fastest sort average
    minimum = 100
    language = ""
    sort = ""
    for l, sortDataDict in languageToData.items():
        for s, data in sortDataDict.items():
            lowest = min(data)
            if lowest < minimum:
                minimum = lowest
                language = l
                sort = s
    
    print(f"The fastest single sort was {language} running {sort} with a time of {minimum} milliseconds!")

    # ranked 
                             
main()




