#!/usr/bin/env python3

# Download Wikipedia view count statistics
# (c) 2015-2016, Matthew Petroff (https://mpetroff.net/)

import requests
import subprocess
import datetime
import os

os.chdir('view_data')

MONTHS = 3

now = datetime.datetime.now()
date_strings = []
for i in range(MONTHS):
    year = now.year
    month = now.month - 1 - i
    if month < 1:
        year -= 1
        month = 12 - month
    date_strings.append(str(year) + '/' + str(year) + '-'
                        + '{0:0>2}'.format(month) + '/')

urls = []

for date in date_strings:
    base_url = 'http://dumps.wikimedia.org/other/pagecounts-raw/' + date
    index = requests.get(base_url + 'md5sums.txt').text
    for line in index.splitlines():
        line = line.split()[1]
        if line[:10] == 'pagecounts':
            urls.append(base_url + line)

for url in sorted(urls):
    subprocess.call(['wget', '-nc', '-c', url])
