from spacepy import pycdf
import bow_shock_model
import numpy as np
import csv
import os
from math import trunc
from dotenv import load_dotenv
from datetime import date, timedelta

#Load in environment variables
load_dotenv("C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Code/data_locations.env")

def sign(x):
    '''
    Returns 1 if x>0, and -1 if x<0
    '''
    return x/abs(x)

def round_half_int(x):
    #Decimal part of the number
    y = (x - trunc(x))**2
    if y >= 0.75**2:
        return(trunc(x) + sign(x))
    elif y < 0.25**2:
        return(trunc(x))
    else:
        return(trunc(x) + 0.5*sign(x))

def binning(data_matrix, bx, by):
    #Check whether values are within the range allowed by the matrix.
    if bx < -20 or bx >= 20:
        #print("B_x out of bounds")
        return data_matrix
    elif by < -20 or by >= 20:
        #print("B_y out of bounds")
        return data_matrix
    else:
        i = int(2*by) + 40
        j = int(2*bx) + 40
        data_matrix[i][j] += 1
        return data_matrix


#80x80 data matrix, containg values for B in the interval -20 nT <= B < 20 nT with resolution 0.5 nT
data_matrix = [[0]*80 for i in range(0, 80)]

            ######### Get data ##########

data_loc = os.getenv("DATA_LOC")

print("Opening CDFs")

for year in range(2014, 2024):
    for day in range(0, 366):
        day_num = str(day)
        year = str(year)
    
        #Day 1 of the year
        strt_date = date(int(year), 1, 1)

        #Convert to date
        res_date = strt_date + timedelta(days=int(day_num) - 1)
        res = res_date.strftime("%Y%m%d")
        
        #Iterate over any possible version number
        for i in range(20, -1, -1):
            if i == 0:
                print("No data file located for date " + res)
                continue
            cdf_path = data_loc + "mvn_insitu_kp-4sec_" + res + "_v" + str(i)+ "_r01.cdf"
            try:
                cdf = pycdf.CDF(cdf_path)
            except pycdf.CDFError:
                continue
            else:
                print("File located for date " + res)
                #Get CDF path
                cdf = pycdf.CDF(cdf_path)

                #Extracts magnetic field components outside magnetosphere
                print("    Extracting data for date " + res)
                for i in range(0, len(cdf['SPICE_spacecraft_MSO'])):
                    #Get position vector
                    x = cdf['SPICE_spacecraft_MSO'][i][0]
                    y = cdf['SPICE_spacecraft_MSO'][i][1]
                    z = cdf['SPICE_spacecraft_MSO'][i][2]

                    if i == 0:
                        print("    Binning data")

                    #Update magnetic field frequency if MAVEN is in the solar wind
                    if bow_shock_model.is_in_solarwind(x, y, z):
                        data_matrix = binning(data_matrix, round_half_int(float(cdf['MAG_field_MSO'][i][0])), round_half_int(float(cdf['MAG_field_MSO'][i][1])))

                break


            ######## Write data to CSV ########

#Binned data location
loc = os.getenv("STORAGE_LOC")

sum = 0
for i in data_matrix:
    for j in i:
        sum += j


#Write the data matrix data to a CSV
print("Writing data")
with open(loc+"binned_xy.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(data_matrix) 

print("Data stored!")