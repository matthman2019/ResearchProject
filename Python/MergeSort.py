# taken from https://www.geeksforgeeks.org/python/python-program-for-merge-sort/
# Edited by Matthew Zielinski

def merge(array : list, left : int, middle : int, right : int):
    # create lengths of the 2 arrays that are being merged
    n1 = middle - left + 1
    n2 = right - middle

    # initialize left and right arrays
    L = [0] * n1
    R = [0] * n2

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






def mergeSort(array : list, left : int = 0, right : int = -1) -> list:
    # default right parameter
    if right == -1:
        right = len(array) - 1
    
    # the divide and conquer part
    if left < right:
        middle = left + (right - left) // 2
        mergeSort(array, left, middle)
        mergeSort(array, middle + 1, right)
        merge(array, left, middle, right)
    
    return array

if __name__ == "__main__":
    array =[e for e in range(250)]
    from random import shuffle
    shuffle(array)
    print("Given array is:", array)

    mergeSort(array)
    print("Sorted array is:", array)