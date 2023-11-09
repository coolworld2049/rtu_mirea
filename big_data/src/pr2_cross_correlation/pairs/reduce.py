#!/usr/bin/python3
import sys

currKey = None
currSum = 0
for line in sys.stdin:
    splitted = line.strip().split("\t")
    if len(splitted) != 2:
        continue

    key = splitted[0]
    if not currKey:
        currKey = key

    if currKey != key:
        print(f"{currKey}\t{currSum}")
        currKey = key
        currSum = 0

    currSum += int(splitted[1])

print(f"{currKey}\t{currSum}")
