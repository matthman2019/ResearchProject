-- It's Lua time!
-- I'm going to be defining most variables local.
-- (That's just how you do it in roblox.)

-- I'll be honest - I forgot that lua for loops are inclusive.
-- I'll be doing my best to elimenate extra iterations,
-- but undoubtedly I'll accidentally have one in here somewhere.
-- this is a source of error.

local lastGenerated = 1
local m = 2 ^ 31 - 1
local a = 7 ^ 5

local function nextNumber()
    lastGenerated = lastGenerated * a % m
    return lastGenerated
end

local function swap(array, i, j)
    local temp = array[i]
    array[i] = array[j]
    array[j] = temp
end

-- One thing I do appreciate about lua is that 
-- it has a dedicated operator for table length: #
-- one thing I DON'T appreciate is 1-based indexing
-- and I REALLY DON'T APPRECIATE INCLUSIVE FOR LOOPS
local function fisherYates(array)
    for i = #array, 1, -1 do
        local j = (nextNumber() % (i)) + 1
        swap(array, i, j)
    end
    return array
end

-- lua has no way to print a table's contents
-- it only prints a table's memory address.
-- this function's only purpose is for debugging.
local function printTable(array)
    local arrayString = "{"
    for _, value in pairs(array) do
        arrayString = arrayString..tostring(value)..", "
    end
    arrayString = arrayString:sub(1, -3).."}"
    print(arrayString)
end

-- there is a solid chance that this function 
-- is running an extra iteration
local function bubbleSort(array)
    local n = #array

    for i = 1, n, 1 do
        local swapped = false
        for j = 1, n-i, 1 do
            if array[j] > array[j+1] then
                swapped = true
                swap(array, j, j+1)
            end
        end
        if not swapped then
            break
        end
    end
    return array
end

local function maximum(array)
    local l = #array
    if l == 0 then
        return
    end
    local max = array[1]

    for i = 1, l, 1 do
        local arrayItem = array[i]
        if arrayItem > max then
            max = arrayItem
        end
    end
    return max
end

-- dangit. I need to initialize tables with zeroes, 
-- but lua won't do that for you. 
-- now this function exists (and it's in my notebook too.)
local function makeTable(length)
    local returnTable = {}
    for i = 1, length, 1 do
        returnTable[i] = 0
    end
    return returnTable
end

local function makeTableWithIndexedKeys(length)
    local returnTable = {}
    for i = 1, length, 1 do
        returnTable[i] = i - 1
    end
    return returnTable
end

-- no way lua doesn't have the += operator. DANGIT
local function countingSort(array, exp1)
    local n = #array

    local output = makeTable(n)
    local count = makeTable(10)

    for i = 1, n, 1 do
        local index = array[i] // exp1
        count[(index % 10) + 1] = count[(index % 10) + 1] + 1
    end

    -- This is funky since indexes change. I hope this works
    for i = 2, 10, 1 do
        count[i] = count[i] + count[i - 1]
    end

    local k = n
    for i = k, 1, -1 do
        local index = array[i] // exp1
        -- no negative table indexes in lua
        local outputIndex = count[(index % 10) + 1]
        if outputIndex == -1 then outputIndex = 10 end
        output[outputIndex] = array[i]
        count[(index % 10) + 1] = count[(index % 10) + 1] - 1
    end

    for i = 1, n, 1 do
        array[i] = output[i]
    end
    return array
end

local function radixSort(array)
    local max1 = maximum(array)

    local exp = 1
    while max1 / exp >= 1 do
        countingSort(array, exp)
        exp = exp * 10
    end

    return array
end

local function insertionSort(array)
    for i = 2, #array, 1 do
        local key = array[i]
        local j = i - 1

        while j >= 1 and key < array[j] do
            array[j + 1] = array[j]
            j = j - 1
        end
        array[j + 1] = key
    end
    return array
end

local function partition(array, low, high)
    local pivot = array[high]
    local i = low - 1

    for j = low, high, 1 do
        if array[j] < pivot then
            i = i + 1
            swap(array, i, j)
        end
    end

    swap(array, i + 1, high)
    return i + 1
end

local function quickSort(array, low, high)
    low = low or 1
    high = high or #array
    if low >= high then return end

    local pi = partition(array, low, high)
    quickSort(array, low, pi - 1)
    quickSort(array, pi + 1, high)
    return array
end

local function merge(array, left, middle, right)
    local n1 = middle - left + 1
    local n2 = right - middle

    local L = makeTable(n1);
    local R = makeTable(n2);

    for i = 1, n1, 1 do
        L[i] = array[left + i - 1]
    end
    for j = 1, n2, 1 do
        R[j] = array[middle + j]
    end
    
    local i = 1
    local j = 1
    local index = left

    while i <= n1 and j <= n2 do
        if L[i] <= R[j] then
            array[index] = L[i]
            i = i + 1
        else
            array[index] = R[j]
            j = j + 1
        end
        index = index + 1
    end
    while i <= n1 do
        array[index] = L[i]
        i = i + 1
        index = index + 1
    end
    while j <= n2 do
        array[index] = R[j]
        j = j + 1
        index = index + 1
    end
end

local function mergeSort(array, left, right)
    left = left or 1
    right = right or #array

    if left < right then
        local middle = (right + left) // 2
        mergeSort(array, left, middle)
        mergeSort(array, middle + 1, right)
        merge(array, left, middle, right)
    end

    return array
end

local function writeToFile(timeList, algorithmName, fileName)
    fileName = fileName or "LuaOutput.txt"
    local file = io.open(fileName, "a")
    if not file then print("Could not open file!"); return end
    file:write("===="..algorithmName.."====\n")
    for _, time in pairs(timeList) do
        file:write(tostring(time).."\n")
    end
end

local function testAlgorithm(algorithm, reps, arrayLength)
    reps = reps or 100
    arrayLength = arrayLength or 4096

    local timeList = {}

    for i = 1, reps, 1 do
        -- this doesn't match the pseudocode, it's not a builtin like python.
        -- it's not timed, however, so it will not affect the end result.
        local array = makeTableWithIndexedKeys(arrayLength)
        fisherYates(array)
        local startTime = os.clock()
        algorithm(array)
        local endTime = os.clock()
        -- os.clock() is in seconds
        table.insert(timeList, (endTime - startTime) * 1000)
    end
    return timeList
end

local function main()
    writeToFile(testAlgorithm(quickSort), "Quick Sort")
    writeToFile(testAlgorithm(insertionSort), "Insertion Sort")
    writeToFile(testAlgorithm(radixSort), "Radix Sort")
    writeToFile(testAlgorithm(mergeSort), "Merge Sort")
    writeToFile(testAlgorithm(bubbleSort), "Bubble Sort")
end

-- we did it ladies and gentlemen
main()