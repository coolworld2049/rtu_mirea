#!/usr/bin/python3
import sys
from collections import defaultdict

currKey = None
resultMap = defaultdict(lambda: 0)
for line in sys.stdin:
    splitted = line.strip().split("\t")
    if len(splitted) != 2:
        continue

    key = splitted[0]
    values = eval(splitted[1])
    if not currKey:
        currKey = key

    if currKey != key:
        for item in resultMap.items():
            print(f"{currKey} {item[0]}\t{item[1]}")
        currKey = key
        resultMap.clear()

    for item in values.items():
        if item[0] != key:
            resultMap[item[0]] += int(item[1])

for item in resultMap.items():
    print(f"{currKey} {item[0]}\t{item[1]}")
