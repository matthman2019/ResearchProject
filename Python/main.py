from BubbleSort import bubbleSort
from FisherYates import fisherYates
from time import perf_counter_ns
from statistics import mean

timeList = []

for i in range(100):
    array = [e for e in range(4096)]
    print(i)
    fisherYates(array)
    
    startTime = perf_counter_ns()
    bubbleSort(array)
    endTime = perf_counter_ns()

    timeList.append(endTime - startTime)

print(mean(timeList) / 1000000)
    