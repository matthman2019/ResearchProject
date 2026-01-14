from LehmerRandomNumberGenerator import nextNumber
import sys

def fisherYates(array : list):

    for i in range(len(array)-1, 0, -1):
        j = nextNumber() % (i+1)

        temp = array[i]
        array[i] = array[j]
        array[j] = temp
    
    return array

if __name__ == "__main__":
    generatedLists = []
    i = 0
    while True:
        shuffledList = tuple(fisherYates([e for e in range(0, 10)]))
        print(shuffledList)
        if shuffledList in generatedLists:
            print(f"Repeat! It took {i} iterations to repeat a list.")
            break
        generatedLists.append(shuffledList)
        i += 1