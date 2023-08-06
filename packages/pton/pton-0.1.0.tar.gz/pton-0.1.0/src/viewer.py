import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap
import geopandas as gpd
import sys

try:
    filename = sys.argv[1]
except:
    filename = '/tmp/city.json'

colors_dic = {1: [0.9, 0.9, 0.2, 1],
              2: [1, 1, 0.5, 1],
              3: [0.25, 0.6, 0.25, 1],
              4: [0.25, 0.75, 0.9, 1],
              5: [0.24, 0.62, 0.92, 1],
              7: [0.35, 0.49, 0.21, 1],
              8: [0.8, 0.9, 0.55, 1],
              10: [0.7, 0.45, 0.25, 1],
              11: [0.5, 0.5, 0.63, 1],
              12: [0.85, 0.5, 0.85, 1],
              15: [0.75, 0.45, 0.15, 1],
              20: [0.6, 0.6, 1, 1],
              21: [0.3, 0.3, 0.8, 1],
              31: [0.4, 0.4, 0.4, 1],
              32: [0.6, 0.6, 0.6, 1],
              33: [1, 1, 1, 1],
              50: [1, 1, 1],
              90: [1, 0, 0, 1]
              }
colors = [[1, 0, 0, 1] for _ in range(max(colors_dic.keys()) + 1)]
for i in colors_dic:
    colors[i] = colors_dic[i]
color_map = ListedColormap(colors, name='Archi')

shapes = gpd.read_file(filename)
fig, ax = plt.subplots(figsize=(20, 16))
shapes.plot(column='category', cmap=color_map,
            k=len(colors) + 1, vmin=0, vmax=len(colors),
            # edgecolor='black',
            aspect='equal', ax=ax)
s = shapes[(shapes.category != 33) & (shapes.category != 1) &
           (shapes.category != 3) & (shapes.category != 4)]
s.geometry.boundary.plot(color=None,
                         edgecolor='white', linewidth=1.5,
                         aspect='equal', ax=ax)

walls = shapes[(shapes.category == 33)]
if len(walls):
    walls.geometry.boundary.plot(color=None,
                                 edgecolor='black', linewidth=2,
                                 aspect='equal', ax=ax)
# plt.grid()
plt.show()
