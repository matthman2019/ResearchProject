from Swap import swap

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

if __name__ == "__main__":
    from random import shuffle
    for i in range(20):
        array = [e for e in range(56)]
        shuffle(array)
        print(bubbleSort(array))