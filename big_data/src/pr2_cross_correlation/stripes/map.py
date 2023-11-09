#!/usr/bin/python3
import sys
from collections import defaultdict

for line in sys.stdin:
    prods = line.strip().split(" ")
    for i in range(len(prods)):
        prodMap = defaultdict(lambda: 0)
        for j in range(len(prods)):
            prodMap[prods[j]] += 1
        print(f"{prods[i]}\t{dict(prodMap)}")
