use Time::HiRes qw(clock_gettime CLOCK_MONOTONIC);
use POSIX qw(floor);

my $lastGenerated = 1;
my $m = 2 ** 31 - 1;
my $a = 7 ** 5;

# this is SO much easier than rust
sub nextNumber {
    $lastGenerated = $lastGenerated * $a % $m;
    return $lastGenerated;
}

# I have to deviate from the pseudocode(ish).
# I will have to access arrays from a pointer EVERY SINGLE TIME.
# I'll still refer to the array parameter as array,
# But its type will now be a referenced array.
sub swap {
    my ($array, $i, $j) = @_;
    my $temp = $$array[$i];
    $$array[$i] = $$array[$j];
    $$array[$j] = $temp;
}

sub fisherYates {
    my $array = shift;
    for (my $i = scalar(@$array) - 1; $i > 0; $i--) {
        my $j = nextNumber() % ($i + 1);
        swap($array, $i, $j);
    }
    return $array;
}

sub bubbleSort {
    my $array = shift;
    my $n = @$array;
    
    for (my $i = 0; $i < $n; $i++) {
        # there are no booleans in perl.
        # I will use 0 and 1 as a substitute.
        my $swapped = 0;
        for (my $j = 0; $j < $n-$i-1; $j++) {
            if ($$array[$j] > $$array[$j + 1]) {
                $swapped = 1;
                swap($array, $j, $j+1);
            }
        }
        if (not $swapped) {
            last;
        }
    }
    return $array
}

sub maximum {
    my $array = shift;
    my $l = @$array;
    if ($l == 0) {
        return $array;
    }
    my $max = $$array[0];

    for (my $i = 0; $i < $l; $i++) {
        my $arrayItem = $$array[$i];
        if ($arrayItem > $max) {
            $max = $arrayItem;
        }
    }
    return $max;
}

sub makeTable {
    my $length = shift;
    my @returnTable = ();
    for (my $i = 0; $i < $length; $i++) {
        push(@returnTable, 0);
    }
    return @returnTable
}

sub makeIndexedTable {
    my $length = shift;
    my @returnTable = ();
    for (my $i = 0; $i < $length; $i++) {
        push(@returnTable, $i);
    }
    return @returnTable

}

sub countingSort {
    my ($array, $exp1) = @_;
    my $n = @$array;
    my @output = makeTable($n);
    my @count = makeTable(10);

    for (my $i = 0; $i < $n; $i++) {
        my $index = floor($$array[$i] / $exp1);
        $count[$index % 10] += 1;
    }
    
    for (my $i = 1; $i < 10; $i++) {
        $count[$i] += $count[$i - 1];
    }
    my $k = $n - 1;
    for (my $i = $k; $i > -1; $i--) {
        my $index = floor($$array[$i] / $exp1);
        $output[$count[$index % 10] - 1] = $$array[$i];
        $count[$index % 10] -= 1;
    }

    for (my $i = 0; $i < $n; $i++) {
        $$array[$i] = $output[$i];
    }
}

sub radixSort {
    my $array = shift;
    my $max1 = maximum($array);
    my $exp = 1;

    while ($max1 / $exp >= 1) {
        countingSort($array, $exp);
        $exp *= 10;
    }
    return $array;
}

sub insertionSort {
    my $array = shift;
    for (my $i = 1; $i < scalar @$array; $i++) {
        my $key = $$array[$i];
        my $j = $i - 1;

        while ($j >= 0 and $key < $$array[$j]) {
            $$array[$j + 1] = $$array[$j];
            $j--;
        }
        $$array[$j + 1] = $key
    }
    return $array
}

sub partition {
    my ($array, $low, $high) = @_;
    my $pivot = $$array[$high];
    my $i = $low - 1;

    for (my $j = $low; $j < $high; $j++) {
        if ($$array[$j] < $pivot) {
            $i++;
            swap($array, $i, $j);
        }
    }
    swap($array, $i + 1, $high);
    return $i + 1;
}

sub quickSort {
    my ($array, $low, $high) = @_;

    if ($high == -1) {
        $high = @$array;
        $high--;
    }
    if ($low >= $high) {
        return $array;
    }

    my $pi = partition($array, $low, $high);

    quickSort($array, $low, $pi - 1);
    quickSort($array, $pi + 1, $high);
    return $array
}

sub quickSortWrapper {
    my $array = shift;
    return quickSort($array, 0, -1);
}

sub merge {
    my ($array, $left, $middle, $right) = @_;
    my $n1 = $middle - $left + 1;
    my $n2 = $right - $middle;

    my @L = makeTable($n1);
    my @R = makeTable($n2);

    for (my $i = 0; $i < $n1; $i++) {
        $L[$i] = $$array[$left + $i];
    }
    for (my $j = 0; $j < $n2; $j++) {
        $R[$j] = $$array[$middle + 1 + $j];
    }

    my $i = 0; my $j = 0;
    my $index = $left;
    while ($i < $n1 and $j < $n2) {
        if ($L[$i] <= $R[$j]) {
            $$array[$index] = $L[$i];
            $i++;
        } else {
            $$array[$index] = $R[$j];
            $j++;
        }
        $index++;
    }
    while ($i < $n1) {
        $$array[$index] = $L[$i];
        $i++;
        $index++;
    }
    while ($j < $n2) {
        $$array[$index] = $R[$j];
        $j++;
        $index++;
    }
}

sub mergeSort {
    my ($array, $left, $right) = @_;
    if ($right == -1) {
        $right = @$array;
        $right--;
    }


    if ($left < $right) {
        my $middle = floor(($right + $left) / 2);
        mergeSort($array, $left, $middle);
        mergeSort($array, $middle + 1, $right);
        merge($array, $left, $middle, $right);
    }
    return $array;
}

sub mergeSortWrapper {
    my $array = shift;
    return mergeSort($array, 0, -1);
}

sub writeToFile {
    my ($timeList, $algorithmName, $fileName) = @_;
    open(my $file, ">>", $fileName);
    print $file ("====" . $algorithmName . "====\n");

    foreach my $time (@$timeList) {
        print $file ($time . "\n");
    }
}

sub writeToFileWrapper {
    my ($array, $algorithmName) = @_;
    writeToFile($array, $algorithmName, "PerlOutput.txt")
}

sub testAlgorithm {
    my ($algorithm, $reps, $arrayLength) = @_;
    my @timeList = ();

    for (my $i = 0; $i < $reps; $i++) {
        @array = makeIndexedTable($arrayLength);
        fisherYates(\@array);
        my $startTime = clock_gettime(CLOCK_MONOTONIC);
        $algorithm -> (\@array);
        my $endTime = clock_gettime(CLOCK_MONOTONIC);
        push(@timeList, ($endTime - $startTime) * 1000);
    }
    return \@timeList;
}

sub testAlgorithmWrapper {
    my $algorithm = shift;
    print("$algorithm\n");
    return testAlgorithm($algorithm, 100, 4096);
}

sub main {
    writeToFileWrapper(testAlgorithmWrapper(\&quickSortWrapper), "Quick Sort");
	writeToFileWrapper(testAlgorithmWrapper(\&insertionSort), "Insertion Sort");
	writeToFileWrapper(testAlgorithmWrapper(\&radixSort), "Radix Sort");
	writeToFileWrapper(testAlgorithmWrapper(\&mergeSortWrapper), "Merge Sort");
	writeToFileWrapper(testAlgorithmWrapper(\&bubbleSort), "Bubble Sort");
}

# here we go ladies and gentlemen
main();