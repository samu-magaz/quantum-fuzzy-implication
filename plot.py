import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

NORM = sys.argv[1]

data = pd.read_csv('data/data_{}.csv'.format(NORM))
tags = data.columns.values.tolist()[2:]

# Prepare plot
data_a = data.a.unique()
data_b = data.b.unique()
X, Y = np.meshgrid(data_a, data_b)
fig = plt.figure()
axs = []
values = np.zeros((len(tags), len(data_a), len(data_b)))

for ia, a in enumerate(data_a):
  for ib, b in enumerate(data_b):
    # For each t-norm
    for it, tag in enumerate(tags):
      values[it][ia][ib] = data[(data.a == a) & (data.b == b)][tag]


for it, tag in enumerate(tags):
  ### For showing all figures
  ax = fig.add_subplot(2, 3, it + 1, projection = '3d', title=tag, xlabel='b', ylabel='a')
  ax.plot_wireframe(X, Y, values[it])
  ax.view_init(azim=-135)
  axs.append(ax)
  ### For saving single figures
  # ax = fig.add_subplot(111, projection = '3d', title=tag, xlabel='b', ylabel='a')
  # ax.set_xlim([0,1])
  # ax.set_ylim([0,1])
  # ax.set_zlim([0,1])
  # ax.plot_wireframe(X, Y, values[it])
  # ax.view_init(azim=255)
  # plt.savefig('figs/{}/{}.png'.format(NORM, tag), bbox_inches='tight')
  # plt.clf()

### 360 Degree view
# for angle in range(0, 360):
#   for ax in axs:
#     ax.view_init(azim=angle-105)
#     plt.draw()
#   plt.pause(0.001)

plt.show()
