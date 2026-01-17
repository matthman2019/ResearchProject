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

if __name__ == "__main__":
    print(maximum([]))
    print(maximum([e for e in range(50)]))

