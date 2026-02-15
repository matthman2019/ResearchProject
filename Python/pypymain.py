def swap(array : list, i : int, j : int):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp

m = (2 ** 31) - 1
a = 7 ** 5

lastGenerated = 1
def nextNumber():
    global lastGenerated
    lastGenerated =  (a * lastGenerated) % m
    return lastGenerated

def fisherYates(array : list):

    for i in range(len(array)-1, 0, -1):
        j = nextNumber() % (i+1)

        temp = array[i]
        array[i] = array[j]
        array[j] = temp
    
    return array

def bubbleSort(array : list):
    n = len(array)

    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if array[j] > array[j+1]:
                swapped = True
                swap(array, j, j+1)
        if not swapped:
            break

    return array

def maximum(array : list):
    l = len(array)
    if l == 0:
        return
    max = array[0]

    for i in range(l):
        arrayItem = array[i]
        if arrayItem > max:
            max = arrayItem
    return max

# I have to make this function because of lua
def makeTable(length):
    returnTable = []
    for i in range(length):
        returnTable.append(0)
    return returnTable

# a necessary prerequisite for radix sort
def countingSort(array : list, exp1 : int):

    n = len(array)

    # The output array elements that will have sorted array
    output = makeTable(n)

    # initialize count array as 0
    count = makeTable(10)

    # Store count of occurrences in count[]
    for i in range(0, n):
        index = array[i] // exp1
        count[index % 10] += 1

    # Change count[i] so that count[i] now contains actual
    # position of this digit in output array
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array
    i = n - 1
    for i in range(i, -1, -1):
        index = array[i] // exp1
        output[count[index % 10] - 1] = array[i]
        count[index % 10] -= 1

    # Copying the output array to array[],
    # so that array now contains sorted numbers
    for i in range(0, n):
        array[i] = output[i]

# Method to do Radix Sort
# note that this modifies array and also returns it
# so radixSort(array) and array = radixSort(array) will both work
def radixSort(array : list) -> list:

    # Find the maximum number to know number of digits
    max1 = maximum(array)

    # Do counting sort for every digit. Note that instead
    # of passing digit number, exp is passed. exp is 10^i
    # where i is current digit number
    exp = 1
    while max1 / exp >= 1:
        countingSort(array, exp)
        exp *= 10
    return array

def insertionSort(array : list) -> list:
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1

        # Move elements of array[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    
    return array

# partition function
def partition(array, low, high):
    
    # choose the pivot
    pivot = array[high]
    
    # index of smaller element and indicates 
    # the right position of pivot found so far
    i = low - 1
    
    # traverse array[low..high] and move all smaller
    # elements to the left side. Elements from low to 
    # i are smaller after every iteration
    for j in range(low, high):
        if array[j] < pivot:
            i += 1
            swap(array, i, j)
    
    # move pivot after smaller elements and
    # return its position
    swap(array, i + 1, high)
    return i + 1

# the QuickSort function implementation
def quickSort(array : list, low : int, high : int) -> list:
    if high == -1:
        high = len(array) - 1
    # base case
    if low >= high:
        return
        
    # pi is the partition return index of pivot
    pi = partition(array, low, high)
    
    # recursion calls for smaller elements
    # and greater or equals elements
    quickSort(array, low, pi - 1)
    quickSort(array, pi + 1, high)
    return array

def quickSortWrapper(array : list) -> list:
    return quickSort(array, 0, -1)

def merge(array : list, left : int, middle : int, right : int):
    # create lengths of the 2 arrays that are being merged
    n1 = middle - left + 1
    n2 = right - middle

    # initialize left and right arrays
    L = makeTable(n1)
    R = makeTable(n2)

    # essentially list splicing
    for i in range(n1):
        L[i] = array[left + i]
    for j in range(n2):
        R[j] = array[middle + 1 + j]

    # i and j are the indexes of L and R for merging.
    # index is the index of array that is being written to.
    i = j = 0
    index = left

    # the actual merging operation
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            array[index] = L[i]
            i += 1
        else:
            array[index] = R[j]
            j += 1
        index += 1

    # once one list is exhausted, finish putting items in the main array
    while i < n1:
        array[index] = L[i]
        i += 1
        index += 1
    while j < n2:
        array[index] = R[j]
        j += 1
        index += 1






def mergeSort(array : list, left : int, right : int) -> list:
    # default right parameter
    if right == -1:
        right = len(array) - 1
    
    # the divide and conquer part
    if left < right:
        middle = (right + left) // 2
        mergeSort(array, left, middle)
        mergeSort(array, middle + 1, right)
        merge(array, left, middle, right)
    
    return array

def mergeSortWrapper(array : list) -> list:
    return mergeSort(array, 0, -1)


from time import perf_counter_ns
# from tqdm import tqdm
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
                fileName : str = "PyPyOutput.txt"):
    with open(fileName, 'a') as file:
        file.write(f"===={algorithmName}====\n")

        for time in timeList:
            file.write(str(time) + "\n")

# tests an algorithm reps number of times
def testAlgorithm(algorithm : Callable[[list], list], 
                  reps : int = 100, 
                  arrayLength : int = 4096):
    # list of times for each sort to complete
    timeList = []

    for i in range(reps):
        # shuffle the input array
        array = [e for e in range(arrayLength)]
        fisherYates(array)
        startTime = perf_counter_ns()
        algorithm(array)
        endTime = perf_counter_ns()
        timeList.append((endTime - startTime) / 1000000)
        print(i)
    return timeList


# the actual code for the program
# There is a way to make this simpler in python 
# (using a list of functions.)
# This won't work in most other languages, however.
# That's why this code is so repetitive.
if __name__ == "__main__":
    
    quickTimes = testAlgorithm(quickSortWrapper)
    writeToFile(quickTimes, "Quick Sort")

    insertionTimes = testAlgorithm(insertionSort)
    writeToFile(insertionTimes, "Insertion Sort")

    radixTimes = testAlgorithm(radixSort)
    writeToFile(radixTimes, "Radix Sort")

    mergeTimes = testAlgorithm(mergeSortWrapper)
    writeToFile(mergeTimes, "Merge Sort")

    bubbleTimes = testAlgorithm(bubbleSort)
    writeToFile(bubbleTimes, "Bubble Sort")
