#include <iostream>
#include <fstream>
#include <chrono>
#include <cmath>
#include <vector>
#include <optional>
#include <string>
#include <cstdint>
using namespace std;

long m = pow(2, 31) - 1;
int a = pow(7, 5);

long lastGenerated = 1;
long nextNumber() {
    lastGenerated = (lastGenerated * a) % m;
    return lastGenerated;
}

void swap(vector<int>& array, int i, int j) {
    int temp = array[i];
    array[i] = array[j];
    array[j] = temp;
}

vector<int> fisherYates(vector<int>& array) {
    for (int i = array.size()-1; i > 0; i--) {
        int j = nextNumber() % (i + 1);
        swap(array, i, j);
    }
    return array;
}

// python will auto-create lists, but I don't know if c++ will.
// this function will not be timed, however, so it will not affect end performance.
vector<int> defaultVector() {
    vector<int> returnVector;
    returnVector.reserve(4096);
    for (int i = 0; i < 4096; i++) {
        returnVector.push_back(i);
    }
    return returnVector;
}

template <typename T>
void printVector(vector<T> array) {
    string returnString = "[";
    for (T thing : array) {
        returnString += to_string(thing);
        returnString += ", ";
    }
    returnString.erase(returnString.length() - 2);
    returnString += "]";
    cout << returnString << endl;
}

vector<int> bubbleSort(vector<int>& array) {
    int n = array.size();

    for (int i = 0; i < n; i++) {
        bool swapped = false;
        for (int j = 0; j < (n-i-1); j++) {
            if (array[j] > array[j + 1]) {
                swapped = true;
                swap(array, j, j+1);
            }
        }
        if (!swapped) {
            break;
        }
    }
    return array;
}

int maximum(vector<int> array) {
    int l = array.size();
    // looking back I could have made the pseudocode !l
    if (l == 0) {
        return 0;
    }
    int max = array[0];

    for (int i = 0; i < l; i++) {
        int arrayItem = array[i];
        if (arrayItem > max) {
            max = arrayItem;
        }
    }
    return max;
}

vector<int> makeTable(int length) {
    vector<int> returnTable = {};
    for (int i = 0; i < length; i++) {
        returnTable.push_back(0);
    }
    return returnTable;
}

void countingSort(vector<int>& array, int exp1) {
    int n = array.size();
    vector<int> output = makeTable(n);
    vector<int> count = makeTable(10);

    for (int i = 0; i < n; i++) {
        int index = floor(array[i] / exp1);
        count[index % 10] += 1;
    }
    for (int i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }

    // renamed variable for safety
    int k = n - 1;
    for (int i = k; i > -1; i--) {
        int index = floor(array[i] / exp1);
        output[count[index % 10] - 1] = array[i];
        count[index % 10] -= 1;
    }

    for (int i = 0; i < n; i++) {
        array[i] = output[i];
    }
}

vector<int> radixSort(vector<int>& array) {
    int max1 = maximum(array);

    // renamed to avoid naming conflict
    int exp1 = 1;
    while (max1 / exp1 >= 1) {
        countingSort(array, exp1);
        exp1 *= 10;
    }
    return array;
}

vector<int> insertionSort(vector<int>& array) {
    for (int i = 1; i < array.size(); i++) {
        int key = array[i];
        int j = i - 1;

        while (j >= 0 && key < array[j]) {
            array[j + 1] = array[j];
            j--;
        }
        array[j + 1] = key;
    }
    return array;
}

int partition(vector<int>& array, int low, int high) {
    int pivot = array[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (array[j] < pivot) {
            i++;
            swap(array, i, j);
        }
    }
    swap(array, i + 1, high);
    return i + 1;
}

vector<int> quickSort(vector<int>& array, int low = 0, int high = -1) {
    if (high == -1) {
        high = array.size() - 1;
    }
    if (low >= high) {
        return array;
    }

    int pi = partition(array, low, high);
    quickSort(array, low, pi - 1);
    quickSort(array, pi + 1, high);
    return array;
}

void merge(vector<int>& array, int left, int middle, int right) {
    int n1 = middle - left + 1;
    int n2 = right - middle;

    vector<int> L = makeTable(n1);
    vector<int> R = makeTable(n2);

    for (int i = 0; i < n1; i++) {
        L[i] = array[left + i];
    }
    for (int j = 0; j < n2; j++) {
        R[j] = array[middle + 1 + j];
    }

    int i = 0, j = 0;
    int index = left;
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
    // I pasted this directly over from javascript
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

vector<int> mergeSort(vector<int>& array, int left = 0, int right = -1) {
    if (right == -1) {
        right = array.size() - 1;
    }

    if (left < right) {
        int middle = floor((right + left) / 2);
        mergeSort(array, left, middle);
        mergeSort(array, middle + 1, right);
        merge(array, left, middle, right);
    }
    return array;
}

void writeToFile(vector<double> timeList, string algorithmName, string fileName = "/home/matthman2019/ResearchProject/C++/C++Output.txt") {
    ofstream File(fileName, std::ios::app);
    File << "====" << algorithmName << "====" << endl;
    for (double time : timeList) {
        File << to_string(time) << endl;
    }
}

// this is different than the pseudocode, and it may affect time.
// c++'s functions have signatures..?
// either way, algorithms like bubble sort have different parameters than merge sort.
// to pass callbacks, I need two different signatures.
// there's probably a more automated way to do this, but I'm not aware of it.

using SortingCallback = vector<int> (*)(vector<int>&);
using HighLowSortingCallback = vector<int> (*)(vector<int>&, int, int);

vector<double> testAlgorithm(SortingCallback algorithm, int reps = 100, int arrayLength = 4096) {
    vector<double> timeList = {};
    timeList.reserve(reps);

    for (int i = 0; i < reps; i++) {
        vector<int> e = defaultVector();
        e = fisherYates(e);

        auto begin = chrono::high_resolution_clock::now();
        algorithm(e);
        auto end = chrono::high_resolution_clock::now();

        
        double elapsed = static_cast<double>(chrono::duration_cast<chrono::nanoseconds>(end - begin).count()) / 1000000.0;
        timeList.push_back(elapsed);
    }
    return timeList;
}

vector<double> testMoreComplicatedAlgorithm(HighLowSortingCallback algorithm, int reps = 100, int arrayLength = 4096) {
    vector<double> timeList = {};
    timeList.reserve(reps);

    for (int i = 0; i < reps; i++) {
        vector<int> e = defaultVector();
        e = fisherYates(e);

        // notice: I have to give algorithm() more parameters. This differs from the pseudocode.
        // I bet it won't affect anything time-wise, but it has the potential to.
        auto begin = chrono::high_resolution_clock::now();
        algorithm(e, 0, -1);
        auto end = chrono::high_resolution_clock::now();

        
        double elapsed = static_cast<double>(chrono::duration_cast<chrono::nanoseconds>(end - begin).count()) / 1000000.0;
        timeList.push_back(elapsed);
    }
    return timeList;
}


// in c++, I don't have to call main()!
int main() {
    writeToFile(testMoreComplicatedAlgorithm(quickSort), "Quick Sort");
    writeToFile(testAlgorithm(insertionSort), "Insertion Sort");
    writeToFile(testAlgorithm(radixSort), "Radix Sort");
    writeToFile(testMoreComplicatedAlgorithm(mergeSort), "Merge Sort");
    writeToFile(testAlgorithm(bubbleSort), "Bubble Sort");
    return 0;
}