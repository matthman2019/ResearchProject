from BubbleSort import bubbleSort
from InsertionSort import insertionSort
from QuickSort import quickSort
from RadixSort import radixSort
from FisherYates import fisherYates
from MergeSort import mergeSort

from time import perf_counter_ns
from tqdm import tqdm
from typing import Callable
import sys
# quickSort has too much recursion (up to 4096!)
# the following line of code fixes this. 
sys.setrecursionlimit(4097)

# this function writes the results to a file.
# it will need to be modified to work in other languages, 
# since they write files in different ways.
def writeToFile(timeList : list, 
                algorithmName : str, 
                fileName : str = "PythonOutput.txt"):
    with open(fileName, 'a') as file:
        file.write(f"===={algorithmName}====\n")

        for time in timeList:
            file.write(str(time) + "\n")

# tests an algorithm reps number of times
def testAlgorithm(algorithm : Callable[[list], list], 
                  reps : int = 100, 
                  arrayLength : int = 2000):
    # list of times for each sort to complete
    timeList = []

    # note: tqdm is entirely to make the console look nice 
    # and to report the progress of the program.
    # it does not need to be added to other languages' programs
    for i in tqdm(range(reps)):
        # shuffle the input array
        array = [e for e in range(arrayLength)]
        fisherYates(array)
        startTime = perf_counter_ns()
        algorithm(array)
        endTime = perf_counter_ns()
        timeList.append(endTime - startTime)
    return timeList


# the actual code for the program
# There is a way to make this simpler in python 
# (using a list of functions.)
# This won't work in most other languages, however.
# That's why this code is so repetitive.
if __name__ == "__main__":
    
    quickTimes = testAlgorithm(quickSort)
    writeToFile(quickTimes, "Quick Sort")

    insertionTimes = testAlgorithm(insertionSort)
    writeToFile(insertionTimes, "Insertion Sort")

    radixTimes = testAlgorithm(radixSort)
    writeToFile(radixTimes, "Radix Sort")

    mergeTimes = testAlgorithm(mergeSort)
    writeToFile(mergeTimes, "Merge Sort")

    bubbleTimes = testAlgorithm(bubbleSort)
    writeToFile(bubbleTimes, "Bubble Sort")