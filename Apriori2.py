import pandas as pd
from itertools import combinations
import time

# Function to read .dat file and return a list of transactions
def read_dat_file(file_path):
    with open(file_path, 'r') as file:
        transactions = [line.strip().split() for line in file.readlines()]
    return transactions

# Parameters
minsup = float(input("Enter Support-Threshold: "))
minconf = float(input("Enter Confidence-Threshold: "))

# Read data from .dat file
file_path = 'data/test.dat'  # Modify this to the correct path of your .dat file
items = read_dat_file(file_path)

# Adjust minsup to actual count
minsup = minsup * len(items)

# Start timing the Apriori algorithm execution
start_time = time.time()

# Creating a list of dictionaries
count = [dict() for x in range(len(max(items, key=len))+1)]

# Count support for each individual item
s = [item for sublist in items for item in sublist]
for item in s:
    if item in count[1]:
        count[1][item] += 1
    else:
        count[1][item] = 1

# Remove infrequent and empty items
for item in list(count[1].keys()):
    if count[1][item] < minsup:
        del count[1][item]

# Generate frequent two item sets
slist = [list() for x in range(33)]
a = combinations(count[1], 2)
for j in a:
    slist[2].append(tuple(sorted(j)))

candidates = []
for itemset in slist[2]:
    candidates.append(itemset)

for itemset in candidates:
    for transaction in items:
        if all(item in transaction for item in itemset):
            if itemset in count[2]:
                count[2][itemset] += 1
            else:
                count[2][itemset] = 1

for itemset in list(count[2].keys()):
    if count[2][itemset] < minsup:
        del count[2][itemset]

# Generate frequent itemsets of length z from z-1
def freq(z):
    for i in count[z-1]:
        for j in count[z-1]:
            a = set(i)
            b = set(j)
            if len(a.intersection(b)) == z-2:
                t = list(combinations(sorted(a.union(b)), z-1))
                c = 0
                for n in t:
                    if n in count[z-1]:
                        c += 1
                if c == z:
                    flag = 0
                    for h in slist[z]:
                        if sorted(list(a.union(b))) == sorted(h):
                            flag = 1
                    if flag == 0:
                        slist[z].append(tuple(sorted(list(a.union(b)))))
    candidates = [tuple(i) for i in slist[z]]
    for itemset in candidates:
        for transaction in items:
            if all(item in transaction for item in itemset):
                if itemset in count[z]:
                    count[z][itemset] += 1
                else:
                    count[z][itemset] = 1
    for itemset in list(count[z].keys()):
        if count[z][itemset] < minsup:
            del count[z][itemset]

# Call function to generate frequent itemsets
i = 3
while len(count[i-1]) != 0:
    freq(i)
    i += 1
q = i - 2

# Function to extract single item set from a tuple
def value(a):
    a = str(a)
    a = a[:-2]
    a = a[2:]
    return a[:-1]

# Find maximal and closed itemsets
maximal = []
closed = []
for i in range(1, q):
    for j in count[i]:
        fm = fc = 0
        for k in count[i+1]:
            a = set(j)
            b = set(k)
            if a.intersection(b) == a:
                fm = 1
                if count[i][j] == count[i+1][k]:
                    fc = 1
        if fm == 0:
            maximal.append(j)
        if fc == 0:
            closed.append(j)
for i in count[q]:
    maximal.append(i)
    closed.append(i)

# Stop timing the Apriori algorithm execution
end_time = time.time()

# Print execution time
execution_time = end_time - start_time
print(f"Execution Time: {execution_time} seconds")

# Find Association Rules 
print("ASSOCIATION RULES")
ant = count.copy()
for i in range(q, 0, -1):
    for j in ant[i]:
        for k in range(i-1, 0, -1):
            s = list(combinations(list(j), k))
            for n in s:
                r = tuple(sorted(set(j).difference(set(n))))
                l = len(n)
                if l == 1:
                    n = value(n)
                    l = 1
                if len(r) == 1:
                    r2 = value(r)
                if n is not None:
                    if (ant[len(j)][j] / ant[l][n]) >= minconf:
                        if n in closed:
                            if len(r) == 1:
                                print(n, "(", ant[l][n], ") --->", r2, "(", ant[len(r)][r2], ") confidence =", (ant[len(j)][j] / ant[l][n]))
                            else:
                                print(n, "(", ant[l][n], ") --->", r, "(", ant[len(r)][r], ") confidence =", (ant[len(j)][j] / ant[l][n]))
