#!/usr/bin/python3
import sys

curr_key = None
curr_sum = 0

for line in sys.stdin:
    key, value = line.strip().split("\t", 1)

    if curr_key != key:
        if curr_key is not None:
            print(f"{curr_key}\t{curr_sum}")
        curr_key = key
        curr_sum = 0

    curr_sum += int(value)

if curr_key is not None:
    print(f"{curr_key}\t{curr_sum}")
