# From https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/
# This code is contributed by Hritik Shah.
# Edited by Matthew Zielinski

# Function to sort array using insertion sort
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

# Driver method
if __name__ == "__main__":
    array = [e for e in range(200)]
    from random import shuffle
    shuffle(array)
    print(insertionSort(array))