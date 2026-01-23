#![allow(warnings)] // Suppresses all warnings in the crate/file

use std::time::Instant;
use std::fs::OpenOptions;
use std::io::Write;

static mut lastGenerated : i64 = 1;
static m : i64 = 2_i64.pow(31) - 1;
static a : i64 = 7_i64.pow(5);


fn nextNumber() -> i32 {
    unsafe {
        lastGenerated = lastGenerated * a % m;
        return lastGenerated as i32;
    }
    
}

fn swap(array : &mut Vec<i32>, i : usize, j : usize) {
    let temp = array[i];
    array[i] = array[j];
    array[j] = temp;
}

fn fisherYates(array : &mut Vec<i32>) -> &mut Vec<i32> {
    for i in (1..(array.len())).rev() {
        let j = nextNumber() % ((i as i32) + 1);
        swap(array, i as usize, j as usize);
    }
    return array;
}

fn bubbleSort(array : &mut Vec<i32>) -> &mut Vec<i32> {
    let n = array.len();

    for i in 0..n {
        let mut swapped = false;
        for j in 0..(n-i-1) {
            if array[j] > array[j + 1] {
                swapped = true;
                swap(array, j, j+1);
            }
        }
        if !swapped {
            break;
        }
    }
    return array;
}

fn maximum(array : &mut Vec<i32>) -> i32 {
    let l = array.len();
    if l == 0 {
        return 0;
    }
    let mut max = array[0];

    for i in 0..l {
        let arrayItem = array[i];
        if arrayItem > max {
            max = arrayItem
        }
    }
    return max;
}

fn makeTable(length : i32) -> Vec<i32> {
    let mut returnTable : Vec<i32> = vec![];
    for i in 0..length {
        returnTable.push(0);
    }
    return returnTable;
}

fn makeIndexedTable(length : i32) -> Vec<i32> {
    let mut returnTable : Vec<i32> = vec![];
    for i in 0..length {
        returnTable.push(i);
    }
    return returnTable;
}

fn countingSort(array : &mut Vec<i32>, exp : i32) {
    let n = array.len();
    let mut output = makeTable(n as i32);
    let mut count = makeTable(10);

    for i in 0..n {
        let index = array[i] / exp;
        count[(index % 10) as usize] += 1;
    }
    for i in 1..10 {
        count[i] += count[i - 1_usize];
    }

    let k = n - 1;
    for i in (0..=k).rev() {
        let index = array[i] / exp;
        output[(count[(index % 10) as usize] - 1) as usize] = array[i];
        count[(index % 10) as usize] -= 1;
    }

    for i in 0..n {
        array[i] = output[i];
    }
}

fn radixSort(array : &mut Vec<i32>) -> &mut Vec<i32> {
    let max1 = maximum(array);
    let mut exp = 1;
    while max1 / exp >= 1 {
        countingSort(array, exp);
        exp *= 10;
    }
    return array;
}

fn insertionSort(array : &mut Vec<i32>) -> &mut Vec<i32> {
    for i in 1..array.len() {
        let key = array[i];
        let mut j = i - 1_usize;
        // due to an error I must deviate from the pseudocode. J is unsigned; it has to be bigger than 0.
        let mut hitZero = false;

        while j >= 0 && key < array[j] {
            array[j + 1] = array[j];
            
            if j == 0 {
                hitZero = true;
                array[0_usize] = key;
                break;
            }
            j -= 1;
        }
        if !hitZero {
            array[(j + 1) as usize] = key;
        }
    }
    return array;
}

fn partition(array : &mut Vec<i32>, low : usize, high : usize) -> usize {
    let pivot = array[high];

    // again, usize can't be less than 0. I have to modify the pseudocode
    let mut i = low;

    for j in low..high {
        if array[j] < pivot {
            swap(array, i, j);
            i += 1;
        }
    }
    swap(array, i, high);
    return i;
}

fn quickSort(array : &mut Vec<i32>, low : i32, high : i32) -> &mut Vec<i32> {
    // I need to modify high. We must deviate from the pseudocode
    let mut realHigh : i32 = high as i32;
    if high == -1 {
        realHigh = (array.len() as i32) - 1;
    }
    if low >= realHigh {
        return array;
    }
    let pi = partition(array, low as usize, realHigh as usize) as i32;
    //println!("{}, {}, {}", low, pi, high);
    quickSort(array, low, pi - 1);
    quickSort(array, pi + 1, realHigh);
    return array;

}

fn quickSortWrapper(array : &mut Vec<i32>) -> &mut Vec<i32> {
    return quickSort(array, 0, -1);
}

fn merge(array : &mut Vec<i32>, left : usize, middle : usize, right : usize) {
    let n1 = middle - left + 1;
    let n2 = right - middle;

    let mut L = makeTable(n1 as i32);
    let mut R = makeTable(n2 as i32);

    for i in 0..n1 {
        L[i] = array[left + i];
    }
    for j in 0..n2 {
        R[j] = array[middle + 1 + j];
    }
    // println!("{:?}, {:?}", L, R);

    let mut i : usize = 0;
    let mut j : usize = 0;
    let mut index = left;

    while i < n1 && j < n2 {
        if L[i] <= R[j] {
            array[index] = L[i];
            i += 1;
        } else {
            array[index] = R[j];
            j += 1;
        }
        index += 1;
        // println!("{:?}", array);
    }
    while i < n1 {
        array[index] = L[i];
        i += 1;
        index += 1;
    }
    while j < n2 {
        array[index] = R[j];
        j += 1;
        index += 1;
    }
}

fn mergeSort(array : &mut Vec<i32>, left : i32, right : i32) -> &mut Vec<i32> {
    // again I must differ from the pseudocode
    let mut realRight = right;
    if right == -1 {
        realRight = (array.len() as i32) - 1;
    }
    if left < realRight {
        let middle = (realRight + left) / 2;
        mergeSort(array, left, middle);
        mergeSort(array, middle + 1, realRight);
        merge(array, left as usize, middle as usize, realRight as usize);
    }
    return array;
}

fn mergeSortWrapper(array : &mut Vec<i32>) -> &mut Vec<i32> {
    return mergeSort(array, 0, -1);
}

fn writeToFile(timeList : Vec<f64>, algorithmName : &str, fileName : &str) {
    let fileReturn = OpenOptions::new().append(true).create(true).open(fileName);
    let mut file = fileReturn.expect("REASON");
    file.write_all(&("====".to_owned() + algorithmName + "====\n").into_bytes());
    for time in timeList.iter() {
        file.write_all(&(time.to_string() + "\n").into_bytes());
    }
}

fn writeToFileWrapped(timeList : Vec<f64>, algorithmName : &str) {
    writeToFile(timeList, algorithmName, "RustOutput.txt");
}

fn runCallback<F: Fn()>(callback : F)
    // where F: Fn(&mut Vec<i32>) -> &mut Vec<i32>,
    {
        callback();
    }

fn testAlgorithm<F>(algorithm : F, reps : i32, arrayLength : i32) -> Vec<f64>
where F: Fn(&mut Vec<i32>) -> &mut Vec<i32>
{
    let mut timeList : Vec<f64> = vec![];

    for i in 0..reps {
        let mut array = makeIndexedTable(arrayLength);
        let mut array = fisherYates(&mut array);
        let startTime = Instant::now();
        algorithm(&mut array);
        let duration = startTime.elapsed();
        let elapsed = duration.as_nanos();
        timeList.push(elapsed as f64 / 1000000.0);
    }

    return timeList;
}

fn testWrapper<F>(algorithm : F) -> Vec<f64>
where F: Fn(&mut Vec<i32>) -> &mut Vec<i32>
{
    return testAlgorithm(algorithm, 100, 4096);
}
fn main() {
    writeToFileWrapped(testWrapper(&quickSortWrapper), "Quick Sort");
    writeToFileWrapped(testWrapper(&insertionSort), "Insertion Sort");
    writeToFileWrapped(testWrapper(&radixSort), "Radix Sort");
    writeToFileWrapped(testWrapper(&mergeSortWrapper), "Merge Sort");
    writeToFileWrapped(testWrapper(&bubbleSort), "Bubble Sort");
}