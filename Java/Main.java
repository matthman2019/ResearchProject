import java.util.ArrayList;
import java.lang.Math;
import java.io.FileWriter;
import java.io.IOException;

interface SortingAlgorithm {
    ArrayList<Integer> run(ArrayList<Integer> array);
}

public class Main {

    // I'll use public methods and variables since that's default in java.
    public static long lastGenerated = 1;
    public static long m = (int) Math.pow(2, 31);
    public static int a = (int) Math.pow(7, 5);

    public static int nextNumber() {
        lastGenerated = (lastGenerated * a) % m;
        return (int) lastGenerated;
    }

    public static void swap(ArrayList<Integer> array, int i, int j) {
        int temp = array.get(i);
        array.set(i, array.get(j));
        array.set(j, temp);

    }

    public static ArrayList<Integer> fisherYates(ArrayList<Integer> array) {
        for (int i = array.size()-1; i > 0; i--) {
            int j = nextNumber() % (i + 1);
            swap(array, i, j);
        }
        return array;
    }

    public static ArrayList<Integer> makeTable(int length) {
        ArrayList<Integer> returnTable = new ArrayList<Integer>();
        for (int i = 0; i < length; i++) {
            returnTable.add(0);
        }
        return returnTable;
    }

    public static ArrayList<Integer> makeIndexedArrayList(int length) {
        ArrayList<Integer> returnTable = new ArrayList<Integer>();
        for (int i = 0; i < length; i++) {
            returnTable.add(i);
        }
        return returnTable;
    }

    public static ArrayList<Integer> bubbleSort(ArrayList<Integer> array) {
        int n = array.size();

        for (int i = 0; i < n; i++) {
            boolean swapped = false;
            for (int j = 0; j < n-i-1; j++) {
                if (array.get(j) > array.get(j + 1)) {
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

    public static int maximum(ArrayList<Integer> array) {
        int l = array.size();
        if (l == 0) {
            return 0;
        }
        int max = array.get(0);

        for (int i = 1; i < l; i++) {
            int arrayItem = array.get(i);
            if (arrayItem > max) {
                max = arrayItem;
            }
        }
        return max;
    }

    public static void countingSort(ArrayList<Integer> array, int exp1) {
        int n = array.size();

        var output = makeTable(n);
        var count = makeTable(10);

        for (int i = 0; i < n; i++) {
            int index = Math.floorDiv(array.get(i), exp1);
            count.set(index % 10, count.get(index % 10) + 1);
        }
        for (int i = 1; i < 10; i++) {
            count.set(i, count.get(i) + count.get(i - 1));
        }

        int k = n - 1;
        for (int i = k; i > -1; i--) {
            int index = Math.floorDiv(array.get(i), exp1);
            output.set(count.get(index % 10) - 1, array.get(i));
            count.set(index % 10, count.get(index % 10) - 1);
        }
        
        for (int i = 0; i < n; i++) {
            array.set(i, output.get(i));
        }
    }

    public static ArrayList<Integer> radixSort(ArrayList<Integer> array) {
        int max1 = maximum(array);

        int exp = 1;
        while (max1 / exp >= 1) {
            countingSort(array, exp);
            exp *= 10;
        }
        return array;
    }

    public static ArrayList<Integer> insertionSort(ArrayList<Integer> array) {
        for (int i = 1; i < array.size(); i++) {
            int key = array.get(i);
            int j = i - 1;

            while (j >= 0 && key < array.get(j)) {
                array.set(j + 1, array.get(j));
                j--;
            }
            array.set(j + 1, key);
        }
        return array;
    }

    public static int partition(ArrayList<Integer> array, int low, int high) {

        int pivot = array.get(high);

        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (array.get(j) < pivot) {
                i++;
                swap(array, i, j);
            }
        }
        swap(array, i+1, high);
        return i + 1;
    }

    // there are no default parameters in java. The closest they have is method overloading.
    // that'll actually solve the callback problem for java and c++.
    public static ArrayList<Integer> quickSort(ArrayList<Integer> array, int low, int high) {
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

    public static void merge(ArrayList<Integer> array, int left, int middle, int right) {
        int n1 = middle - left + 1;
        int n2 = right - middle;

        ArrayList<Integer> L = makeTable(n1);
        ArrayList<Integer> R = makeTable(n2);

        for (int i = 0; i < n1; i++) {
            L.set(i, array.get(left + i));
        }
        for (int j = 0; j < n2; j++) {
            R.set(j, array.get(middle + 1 + j));
        }

        int i = 0, j = 0;
        int index = left;

        while (i < n1 && j < n2) {
            if (L.get(i) <= R.get(j)) {
                array.set(index, L.get(i));
                i++;
            }
            else {
                array.set(index, R.get(j));
                j++;
            }
            index++;
        }
        while (i < n1) {
            array.set(index, L.get(i));
            i++;
            index++;
        }
        while (j < n2) {
            array.set(index, R.get(j));
            j++;
            index++;
        }
    }

    public static ArrayList<Integer> mergeSort(ArrayList<Integer> array, int left, int right) {
        if (right == -1) {
            right = array.size() - 1;
        }
        if (left < right) {
            int middle = Math.floorDiv(right + left, 2);
            mergeSort(array, left, middle);
            mergeSort(array, middle + 1, right);
            merge(array, left, middle, right);
        }
        return array;
    }

    public static void writeToFile(ArrayList<Double> timeList, String algorithmName, String fileName) {
        // java is forcing me to use try and except here
        try {
            FileWriter file = new FileWriter(fileName, true);
            file.write("====" + algorithmName + "====\n");
            for (double time : timeList) {
                file.write(String.valueOf(time) + "\n");
            }
            file.close();
        } catch (IOException e) {
            System.out.println("Could not write to file!");
        }
    }

    public static void writeToFile(ArrayList<Double> timeList, String algorithmName) {
        writeToFile(timeList, algorithmName, "JavaOutput.txt");
    }

    // Java doesn't really like callbacks the way python can. Interfaces are a good substitute.
    public static ArrayList<Double> testAlgorithm(SortingAlgorithm algorithm, int reps, int arrayLength) {
        ArrayList<Double> timeList = new ArrayList<Double>();

        for (int i = 0; i < reps; i++) {
            ArrayList<Integer> array = makeIndexedArrayList(arrayLength);
            fisherYates(array);
            long startTime = System.nanoTime();
            algorithm.run(array);
            long endTime = System.nanoTime();
            timeList.add(((double)(endTime - startTime)) / 1000000.0);
        }

        return timeList;
    }
    public static ArrayList<Double> testAlgorithm(SortingAlgorithm algorithm) {
        return testAlgorithm(algorithm, 100, 4096);
    }

    public static void main(String[] args) {
        //SortingAlgorithm quickSort = ;
        writeToFile(testAlgorithm((array) -> quickSort(array, 0, -1)), "Quick Sort");
        writeToFile(testAlgorithm((array) -> insertionSort(array)), "Insertion Sort");
        writeToFile(testAlgorithm((array) -> radixSort(array)), "Radix Sort");
        writeToFile(testAlgorithm((array) -> mergeSort(array, 0, -1)), "Merge Sort");
        writeToFile(testAlgorithm((array) -> bubbleSort(array)), "Bubble Sort");

    }



}