#!/usr/bin/python3
import sys

for line in sys.stdin:
    products = line.strip().split(" ")
    for i in range(len(products)):
        for j in range(i + 1, len(products)):
            print(f"{max(products[i], products[j])} {min(products[i], products[j])}\t1")
