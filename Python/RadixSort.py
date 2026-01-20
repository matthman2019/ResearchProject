# taken from https://www.geeksforgeeks.org/dsa/radix-sort/
# This code is contributed by Mohit Kumra
# Edited by Patrick Gallagher
# Further edited by Matthew Zielinski

from Max import maximum

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

if __name__ == "__main__":

    from random import shuffle
    arr = [e for e in range(0, 200, 2)]
    shuffle(arr)
    print(radixSort(arr))


    #countingSort([1, 2, 22, 33, 43, 303, 5, 99, 10], 1)