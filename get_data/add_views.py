#!/usr/bin/env python3

# Add Wikipedia view counts to data
# (c) 2015-2016, Matthew Petroff (https://mpetroff.net/)

import pickle
import gzip
import numpy as np

with gzip.open('data.pkl.gz', 'rb') as pkl_file:
    data = pickle.load(pkl_file)

with gzip.open('view_stats.pkl.gz', 'rb') as pkl_file:
    views = pickle.load(pkl_file)

for dimension in data:
    data[dimension].append(np.zeros(len(data[dimension][1]), np.uint32))
    for i in range(len(data[dimension][1])):
        if data[dimension][1][i] in views:
            data[dimension][-1][i] = views[data[dimension][1][i]]

with gzip.open('data_with_views.pkl.gz', 'wb') as output:
    pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
