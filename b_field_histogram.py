'''
Plots:
    A histogram of the magnetic field strength between 0 and 20 nT
    A 2D histogram of the magnetic field in the x-y plane
'''

import matplotlib.pyplot as plt 
import csv, os, maths_tools
from dotenv import load_dotenv


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
bs = [maths_tools.round_half_int(float(b[i][0])) for i in range(len(b))]
freq = [int(b[i][1]) for i in range(len(b))]

bs_half_int = []
freq_half_int = []

#Re-bin data to integer values
for b in bs:
    i = bs.index(b)
    if b in bs_half_int:
        j = bs_half_int.index(b)
        freq_half_int[j] += freq[i]
    else:
        bs_half_int.append(b)
        freq_half_int.append(freq[i])

#Add extra row as endpoint for step plot
bs_half_int.append(bs_half_int[-1]+0.5)

        ######### bx/by preprocessing ########

#Reverse the list so that B_y decreases along the vertical axis
matrix = matrix[::-1]

        ######## Plotting ########

#Initialise figure
fig, (ax1, ax2) = plt.subplots(2, 1)

fig.suptitle("Magnetic field distribution")

            ######## Histogram of magnitude ########

#Plot magnitudes
ax1.stairs(freq_half_int, bs_half_int, color = 'xkcd:black')

#Title
ax1.set_xlabel("$|B|$ (nT)")
ax1.set_ylabel("Frequency")
ax1.minorticks_on()
ax1.set_xlim([0, 20])

#Plot x-y data
h = ax2.imshow(matrix, cmap = 'binary', extent = [-20, 20, -20, 20])
ax2.set_xlabel("$B_x$ (nT)")
ax2.set_ylabel("$B_y$ (nT)")
ax2.minorticks_on()

#Colorbar
fig.colorbar(h, ax=ax2, label = 'Frequency')

plt.show()