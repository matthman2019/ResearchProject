package main

import (
	"math"
	"os"
	"strconv"
	"time"
)

var m = int(math.Pow(2, 31) - 1)
var a = int(math.Pow(7, 5))
var lastGenerated = 1

type sortingAlgorithm func(array []int) []int

func nextNumber() int {
	lastGenerated = lastGenerated * a % m
	return lastGenerated
}

// I HAVE to use a pointer here.
func swap(arrayPtr *[]int, i int, j int) {
	array := *arrayPtr
	temp := array[i]
	array[i] = array[j]
	array[j] = temp
}

func fisherYates(array []int) []int {
	for i := len(array) - 1; i > 0; i-- {
		j := nextNumber() % (i + 1)
		swap(&array, i, j)
	}
	return array
}

func bubbleSort(array []int) []int {
	n := len(array)

	for i := 0; i < n; i++ {
		swapped := false
		for j := 0; j < n-i-1; j++ {
			if array[j] > array[j+1] {
				swapped = true
				swap(&array, j, j+1)
			}
		}
		if !swapped {
			break
		}
	}
	return array
}

func maximum(array []int) int {
	l := len(array)
	if l == 0 {
		return 0
	}
	max := array[0]
	for i := 0; i < l; i++ {
		arrayItem := array[i]
		if arrayItem > max {
			max = arrayItem
		}
	}
	return max
}

func makeTable(length int) []int {
	returnTable := make([]int, 0, length)
	for i := 0; i < length; i++ {
		returnTable = append(returnTable, 0)
	}
	return returnTable
}

func makeIndexedTable(length int) []int {
	returnTable := make([]int, 0, length)
	for i := 0; i < length; i++ {
		returnTable = append(returnTable, i)
	}
	return returnTable
}

func countingSort(arrayPtr *[]int, exp1 int) {
	array := *arrayPtr
	n := len(array)
	output := makeTable(n)
	count := makeTable(10)

	for i := 0; i < n; i++ {
		// I know it doesn't match the pseudocode, but go won't let me use floor division
		// it's an int divided by an int, so the result is also an int
		index := array[i] / exp1
		count[index%10] += 1
	}
	for i := 1; i < 10; i++ {
		count[i] += count[i-1]
	}

	i := n - 1
	for i := i; i > -1; i-- {
		index := array[i] / exp1
		output[count[index%10]-1] = array[i]
		count[index%10] -= 1
	}
	for i = 0; i < n; i++ {
		array[i] = output[i]
	}
}

func radixSort(array []int) []int {
	max1 := maximum(array)
	exp := 1
	// here we get to funny go syntax.
	// there are no while loops, only for loops.
	// but you can override for loops to make them while loops.
	for max1/exp >= 1 {
		countingSort(&array, exp)
		exp *= 10
	}
	return array
}

func insertionSort(array []int) []int {
	for i := 1; i < len(array); i++ {
		key := array[i]
		j := i - 1
		for j >= 0 && key < array[j] {
			array[j+1] = array[j]
			j -= 1
		}
		array[j+1] = key
	}
	return array
}

func partition(arrayPtr *[]int, low int, high int) int {
	array := *arrayPtr
	pivot := array[high]
	i := low - 1
	for j := low; j < high; j++ {
		if array[j] < pivot {
			i++
			swap(arrayPtr, i, j)
		}
	}
	swap(arrayPtr, i+1, high)
	return i + 1
}

func quickSort(array []int, low int, high int) []int {
	if high == -1 {
		high = len(array) - 1
	}
	if low >= high {
		return array
	}

	pi := partition(&array, low, high)
	quickSort(array, low, pi-1)
	quickSort(array, pi+1, high)
	return array
}

func quickSortWrap(array []int) []int {
	return quickSort(array, 0, -1)
}

func merge(arrayPtr *[]int, left int, middle int, right int) {
	array := *arrayPtr
	n1 := middle - left + 1
	n2 := right - middle

	L := makeTable(n1)
	R := makeTable(n2)

	for i := 0; i < n1; i++ {
		L[i] = array[left+i]
	}
	for j := 0; j < n2; j++ {
		R[j] = array[middle+1+j]
	}

	var i, j int = 0, 0
	index := left
	for i < n1 && j < n2 {
		if L[i] <= R[j] {
			array[index] = L[i]
			i++
		} else {
			array[index] = R[j]
			j++
		}
		index++
	}
	for i < n1 {
		array[index] = L[i]
		i++
		index++
	}
	for j < n2 {
		array[index] = R[j]
		j++
		index++
	}
}

func mergeSort(array []int, left int, right int) []int {
	if right == -1 {
		right = len(array) - 1
	}

	if left < right {
		middle := (right + left) / 2
		mergeSort(array, left, middle)
		mergeSort(array, middle+1, right)
		merge(&array, left, middle, right)
	}
	return array
}

func mergeSortWrap(array []int) []int {
	return mergeSort(array, 0, -1)
}

func writeToFile(timeList []float64, algorithmName string, fileName string) {
	file, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		panic(err)
	}

	defer file.Close()
	file.WriteString("====" + algorithmName + "====\n")
	for _, value := range timeList {
		file.WriteString(strconv.FormatFloat(value, 'g', 20, 64) + "\n")
	}
}

func wrappedWrite(timeList []float64, algorithmName string) {
	writeToFile(timeList, algorithmName, "GoOutput.txt")
}

func testAlgorithm(algorithm sortingAlgorithm, reps int, arrayLength int) []float64 {
	timeList := make([]float64, 0, reps)

	for i := 0; i < reps; i++ {
		array := makeIndexedTable(arrayLength)
		array = fisherYates(array)
		startTime := time.Now().UnixNano()
		algorithm(array)
		endTime := time.Now().UnixNano()
		timeList = append(timeList, (float64(endTime)-float64(startTime))/1000000.0)
	}
	return timeList
}

func testAlgorithmWrap(algorithm sortingAlgorithm) []float64 {
	return testAlgorithm(algorithm, 100, 4096)
}

func main() {
	wrappedWrite(testAlgorithmWrap(quickSortWrap), "Quick Sort")
	wrappedWrite(testAlgorithmWrap(insertionSort), "Insertion Sort")
	wrappedWrite(testAlgorithmWrap(radixSort), "Radix Sort")
	wrappedWrite(testAlgorithmWrap(mergeSortWrap), "Merge Sort")
	wrappedWrite(testAlgorithmWrap(bubbleSort), "Bubble Sort")

}
