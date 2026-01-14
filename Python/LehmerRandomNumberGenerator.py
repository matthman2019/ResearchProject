m = (2 ** 31) - 1
a = 7 ** 5

lastGenerated = 1
def nextNumber():
    global lastGenerated
    lastGenerated =  (a * lastGenerated) % m
    return lastGenerated
'''
seed = 0.5
values = [0.5]
errorTolerance = 0.0000001
timesRepeated = 0
while True:
    # print(seed)
    seed = lehmer(seed)

    # find repeat
    values.sort()
    for value in values:
        if seed < value:
            break
    if abs(value - seed) < errorTolerance:
        timesRepeated += 1
    else:
        timesRepeated = 0
    
    if timesRepeated > 2:
        print(f"Repeated {timesRepeated} times!")
        break
    
    values.append(seed)

print(f"{len(values)} values generated!")

'''
if __name__ == "__main__":
    for i in range(30):
        print(nextNumber())