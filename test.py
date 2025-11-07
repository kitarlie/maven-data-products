import matplotlib.pyplot as plt 
import numpy as np
import math
import csv
import os
from dotenv import load_dotenv
from matplotlib import cm
import matplotlib.cbook as cbook
import matplotlib.colors as colors

mylist = [
    [1, 2, 3, 4],
    [5, 6, 7, 8]
]

fig, ax = plt.subplots(1, 1)

ax.imshow(mylist)

plt.show()