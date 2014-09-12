#!/usr/bin/env python3

# Process saved DBpedia data
# (c) 2014, Matthew Petroff (http://mpetroff.net/)

import csv
import glob
import pickle
import math
import gzip
import numpy as np

d = {
    'area': [],
    'density': [],
    'frequency': [],
    'length': [],
    'mass': [],
    'power': [],
    'voltage': [],
    'speed': [],
    'temperature': [],
    'time': [],
    'torque': [],
    'volume': []
}

# Read input
for f in glob.glob('data/*.csv'):
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile)
        parts = f.split('/')[1].split('.')
        for row in reader:
            f = float(row[2])
            # Throw out invalid entries
            if not math.isnan(f) and f > 0:
                d[parts[0]].append([row[0], row[1], f, parts[1]])

# Sort by value
for k in d:
    d[k] = sorted(d[k], key=lambda i: i[2])
    d[k] = list(zip(*d[k]))
    d[k][2] = np.array(d[k][2])
    # Remove URL cruft
    d[k][1] = list(d[k][1])
    for i in range(len(d[k][1])):
        d[k][1][i] = d[k][1][i].replace('http://en.wikipedia.org/wiki/', '')
    d[k][1] = tuple(d[k][1])

output = gzip.open('data.pkl.gz', 'wb')
pickle.dump(d, output, pickle.HIGHEST_PROTOCOL)
output.close()
