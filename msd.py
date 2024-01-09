import sys
import numpy as np
import pandas as pd
import csv

NORM = sys.argv[1]

data = pd.read_csv('data/data_{}.csv'.format(NORM))
tags = data.columns.values.tolist()[2:]

with open('data/msd_{}.csv'.format(NORM), 'w', encoding='UTF8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONE)
    writer.writerow(tags)

    for left in tags:
      row = []
      for right in tags:
        row.append(np.square(data[left] - data[right]).mean())
      writer.writerow(['{:.5f}'.format(r) for r in row])