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

# now we create the file
with open("meanoutput.csv", "w") as file:
    # Header
    sampleData = languageToData["Go"]

    file.write(",")
    for sortName in sampleData.keys():
        file.write(sortName + ",")
    file.write('\n')

    # write each language
    for languageName, languageData in languageToData.items():
        file.write(languageName + ",")
        for dataValues in languageData.values():
            file.write(f"{mean(dataValues)},")
        file.write("\n")

print("Success!")





