import matplotlib.pyplot as plt 
import numpy as np
import math
import csv
import os
from dotenv import load_dotenv
from matplotlib import cm
import matplotlib.cbook as cbook
import matplotlib.colors as colors


#Load in environment variables
load_dotenv("C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Code/data_locations.env")

#Initialise arrays
matrix = []
b = []

#Binned data location
loc = os.getenv("STORAGE_LOC")

#Read in magnitudes
with open(loc+"binned_mag.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 

    fields = next(csvreader)
    for row in csvreader:  
        if len(row) != 0:   
            b.append(row)

#Read in x-y matrix
with open(loc+"binned_xy.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 

    fields = next(csvreader)
    for row in csvreader:  
        if len(row) != 0:
            row_ints = [int(x) for x in row]   
            matrix.append(row_ints)

        ######### Magnitude preprocessing ########

#Split into two separate lists
bs = [math.trunc(float(b[i][0])) for i in range(len(b))]
freq = [int(b[i][1]) for i in range(len(b))]

bs_int = []
freq_int = []

#Re-bin data to integer values
for b in bs:
    i = bs.index(b)
    if b in bs_int:
        j = bs_int.index(b)
        freq_int[j] += freq[i]
    else:
        bs_int.append(b)
        freq_int.append(freq[i])

#Add extra row as endpoint for step plot
bs_int.append(bs_int[-1]+1)



        ######## Plotting ########

#Initialise figure
fig, (ax1, ax2) = plt.subplots(2, 1)

fig.suptitle("Magnetic field distribution")

            ######## Histogram of magnitude ########

#Plot magnitudes
ax1.stairs(freq_int, bs_int, color = 'xkcd:black')

#Title
ax1.set_xlabel("$|B|$ (nT)")
ax1.set_ylabel("Frequency")
ax1.minorticks_on()
ax1.set_xlim([0, 20])

#Plot x-y data
h = ax2.imshow(matrix, cmap = 'plasma', extent = [-20, 20, -20, 20])
ax2.set_xlabel("$B_x$ (nT)")
ax2.set_ylabel("$B_y$ (nT)")
ax2.minorticks_on()

#Colorbar
fig.colorbar(h, ax=ax2, label = 'Frequency')

plt.show()