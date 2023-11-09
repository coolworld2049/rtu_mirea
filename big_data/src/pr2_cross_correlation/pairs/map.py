#!/usr/bin/python3
import sys

for line in sys.stdin:
    products = line.strip().split()
    n = len(products)

    for i in range(n):
        for j in range(i + 1, n):
            product1, product2 = products[i], products[j]
            if product1 < product2:
                print(f"{product1} {product2}\t1")
            else:
                print(f"{product2} {product1}\t1")
