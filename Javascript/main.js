// Zielinski Research Project

// Lehmer Random Number Generator
let lastGenerated = 1;
let m = 2 ** 31 - 1
let a = 7 ** 5
function nextNumber() {
    lastGenerated = lastGenerated * a % m;
    return lastGenerated;
};

function swap(array, i, j) {
    temp = array[i];
    array[i] = array[j];
    array[j] = temp;
};

function fisherYates(array) {
    for (let i = array.length-1; i > 0; i--) {
        j = nextNumber() % (i + 1);
        swap(array, i, j);
    };
    return array;
}

function bubbleSort(array) {
    n = array.length
    for (let i = 0; i < n; i++) {
        let swapped = false;

        for (let j = 0; j < n - i - 1; j++) {
            if (array[j] > array[j+1]) {
                swapped = true;
                swap(array, j, j+1);
            };
        };
        if (!swapped) {
            break;
        }
    }
    return array;
}

function maximum(array) {
    let l = array.length;
    if (l == 0) {
        return;
    }
    let max = array[0];

    for (let i = 0; i < l; i++) {
        let arrayItem = array[i];
        if (arrayItem > max) {
            max = arrayItem;
        };
    };
    return max;
}

// I have to have this because of Lua.
// In Lua's (dis)honor, I'm naming this makeTable
// instead of makeArray or the like.
function makeTable(length) {
    let returnTable = [];
    for (let i = 0; i < length; i++) {
        returnTable.push(0);
    }
    return returnTable;
}

function countingSort(array, exp1) {
    n = array.length;

    output = makeTable(n);
    count = makeTable(10);

    for (let i = 0; i < n; i++) {
        // javascript doesn't have floor division like python
        let index = Math.floor(array[i] / exp1);
        count[index % 10] += 1;
    }
    for (let i = 1; i < 10; i++) {
        // I have to use the at() method for negative indexes
        count[i] += count.at(i-1);
    }

    let k = n - 1; // I renamed this variable from the original python
    for (let i = k; i > -1; i--) {
        index = Math.floor(array[i] / exp1);
        output[count[index % 10] - 1] = array[i];
        count[index % 10] -= 1;
    }

    for (let i = 0; i < n; i++) {
        array[i] = output[i];
    }
}

function radixSort(array) {
    max1 = maximum(array);

    let exp = 1;
    while (max1 / exp >= 1) {
        countingSort(array, exp);
        exp *= 10;
    }
    return array;
};

function insertionSort(array) {
    for (let i = 1; i < array.length; i++) {
        let key = array[i];
        let j = i - 1;

        while (j >= 0 && key < array[j]) {
            array[j + 1] = array[j];
            j -= 1;
        }
        array[j + 1] = key;
    }
    return array;
}

function partition(array, low, high) {
    let pivot = array[high];
    let i = low - 1;
    for (let j = low; j < high; j++) {
        if (array[j] < pivot) {
            i += 1;
            swap(array, i, j);
        }
    }
    swap(array, i + 1, high);
    return i + 1;
}

function quickSort(array, low, high) {
    if (high == -1) {
        high = array.length - 1;
    }
    if (low >= high) {
        return;
    }
    let pi = partition(array, low, high);
    quickSort(array, low, pi-1);
    quickSort(array, pi+1, high);
    return array;
}

function quickSortWrapped(array) {
    return quickSort(array, 0, -1)
}

function merge(array, left, middle, right) {
    let n1 = middle - left + 1;
    let n2 = right - middle;

    L = makeTable(n1);
    R = makeTable(n2);

    for (let i = 0; i < n1; i++) {
        L[i] = array[left + i];
    }
    for (let j = 0; j < n1; j++) {
        R[j] = array[middle + 1 + j];
    }

    let i = 0;
    let j = 0;
    let index = left;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            array[index] = L[i];
            i++;
        }
        else {
            array[index] = R[j];
            j++;
        }
        index++;
    }

    while (i < n1) {
        array[index] = L[i];
        i++;
        index++;
    }
    while (j < n2) {
        array[index] = R[j];
        j++;
        index++;
    }
}

function mergeSort(array, left=0, right=-1) {
    if (right == -1) {
        right = array.length - 1;
    }

    if (left < right) {
        let middle = Math.floor((right + left) / 2);
        mergeSort(array, left, middle);
        mergeSort(array, middle+1, right);
        merge(array, left, middle, right);
    }
    return array;
}

function mergeSortWrapper(array) {
    return mergeSort(array)
}

// I though javascript couldn't write files, but it CAN with node.js!
// gemini is hard carrying this function

const fsPromises = require('fs/promises');
function writeToFile(timeList, algorithmName, fileName="JavascriptOutput.txt") {
    fsPromises.appendFile(fileName, "====" + algorithmName + "====\n", 'utf-8');
    for (const time of timeList) {
        fsPromises.appendFile(fileName, time.toString() + "\n", 'utf-8');
    }
}

function testAlgorithm(algorithm, reps=100, arrayLength = 4096) {
    timeList = []

    for (let i = 0; i < reps; i++) {
        // from gemini.
        let array = Array.from({ length: 4096 }, (value, index) => index);
        fisherYates(array);
        const startTime = performance.now();
        algorithm(array);
        const endTime = performance.now();
        timeList.push(endTime - startTime);
    }
    return timeList
}


function main() {
    writeToFile(testAlgorithm(quickSortWrapped), "Quick Sort");
    writeToFile(testAlgorithm(insertionSort), "Insertion Sort");
    writeToFile(testAlgorithm(radixSort), "Radix Sort");
    writeToFile(testAlgorithm(mergeSortWrapper), "Merge Sort");
    writeToFile(testAlgorithm(bubbleSort), "Bubble Sort");
}

// ladies and gentlemen
// we did it
main();
