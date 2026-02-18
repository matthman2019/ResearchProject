from pathlib import Path

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
with open("output.csv", "w") as file:
    # Header
    sampleData = languageToData["Go"]

    file.write(",")
    for sortName in sampleData.keys():
        file.write(sortName + ",")
        for i in range(len(sampleData[sortName])):
            file.write(",")
    file.write('\n')

    # write each language
    for languageName, languageData in languageToData.items():
        file.write(languageName + ",")
        for dataValues in languageData.values():
            for datum in dataValues:
                file.write(f"{datum},")
        file.write("\n")

print("Success!")





