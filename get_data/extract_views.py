#!/usr/bin/env python3

# Extract Wikipedia view counts
# (c) 2015-2016, Matthew Petroff (https://mpetroff.net/)

import glob
import gzip
import pickle

with gzip.open('data.pkl.gz', 'rb') as pkl_file:
    data = pickle.load(pkl_file)

print('Loading page information...')

pages = {}
for dimension in data:
    for i in range(len(data[dimension][1])):
        pages[data[dimension][1][i]] = 0

print('Processing view data...')

for stat_file_name in sorted(glob.glob('view_data/pagecounts-*')):
    print(stat_file_name)
    with gzip.open(stat_file_name, 'rt') as stat_file:
        for line in stat_file.readlines():
            line = line.split()
            if line[0] == 'en' and line[1] in pages:
                pages[line[1]] += int(line[2])

with gzip.open('view_stats.pkl.gz', 'wb') as output:
    pickle.dump(pages, output, pickle.HIGHEST_PROTOCOL)
