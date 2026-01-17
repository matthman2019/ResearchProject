# taken from https://www.geeksforgeeks.org/dsa/quick-sort-algorithm/
# Edited by Matthew Zielinski
from Swap import swap

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
def quickSort(array : list, low : int = 0, high : int = -1) -> list:
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

if __name__ == "__main__":
    array = [e for e in range(200)]
    from random import shuffle
    shuffle(array)
    n = len(array)
    print(quickSort(array, 0, n - 1))
