from spacepy import pycdf
import bow_shock_model
import numpy as np
import csv
import os
from dotenv import load_dotenv
from datetime import date, timedelta

#Load in environment variables
load_dotenv("C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Code/data_locations.env")

def bin_values(list, binned, keys):
    for x in list:
        if x in keys:
            binned[keys.index(x)] += 1
        else:
            keys.append(x)
            binned.append(1)
    
    return binned, keys


            ######## Create global lists ########

            ######### Create eached binned list ########

binned_x = []
binned_y = []
binned_z = []
binned_mag = []

            ######### Create list of bin keys ########

x_keys = []
y_keys = []
z_keys = []
mag_keys = []
 
            ######### Get data ##########

data_loc = os.getenv("DATA_LOC")

print("Opening CDFs")

for year in range(2014, 2025):
    #Ensure loop gets killed at the end
    if year == 2024:
        break
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

                #Components of detected magnetic field vector in Mars-Solar-Orbital coordinates
                bxs = []
                bys = []
                bzs = []

                #Extracts magnetic field components outside magnetosphere
                print("    Extracting data for date " + res)
                for i in range(0, len(cdf['SPICE_spacecraft_MSO'])):
                    #Get position vector
                    x = cdf['SPICE_spacecraft_MSO'][i][0]
                    y = cdf['SPICE_spacecraft_MSO'][i][1]
                    z = cdf['SPICE_spacecraft_MSO'][i][2]

                    #Append magnetic field data if MAVEN is in the solar wind
                    if bow_shock_model.is_in_solarwind(x, y, z):

                        bxs.append(cdf['MAG_field_MSO'][i][0])
                        bys.append(cdf['MAG_field_MSO'][i][1])
                        bzs.append(cdf['MAG_field_MSO'][i][2])

                #Magnitude of magnetic field
                bs = [np.sqrt(bxs[i]**2 + bys[i]**2 + bzs[i]**2) for i in range(len(bxs))]

                #Round the lists to one decimal place
                bxs = np.round(bxs, decimals = 1)
                bys = np.round(bys, decimals = 1)
                bzs = np.round(bzs, decimals = 1)
                bs = np.round(bs, decimals = 1)

                print("    Binning data")

                #Add the lists to the bins
                binned_x, x_keys = bin_values(bxs, binned_x, x_keys)
                binned_y, y_keys = bin_values(bys, binned_y, y_keys)
                binned_z, z_keys = bin_values(bzs, binned_z, z_keys)
                binned_mag, mag_keys = bin_values(bs, binned_mag, mag_keys)

                break

#Combine values and keys into one list.
bx = [[x_keys[i], binned_x[i]] for i in range(len(binned_x))]
by = [[y_keys[i], binned_y[i]] for i in range(len(binned_y))]
bz = [[z_keys[i], binned_z[i]] for i in range(len(binned_z))]
b = [[mag_keys[i], binned_mag[i]] for i in range(len(binned_mag))]

bx = sorted(bx)
by = sorted(by)
bz = sorted(bz)
b = sorted(b)

if b[-1][0] == np.inf:
    b.pop(-1)

#Binned data location
loc = os.getenv("STORAGE_LOC")

#Write the x-component data to a CSV
with open(loc+"binned_x.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["bx", "frequency"])
    csvwriter.writerows(bx) 

#Write the y-component data to a CSV
with open(loc+"binned_y.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["by", "frequency"])
    csvwriter.writerows(by) 

#Write the z-component data to a CSV
with open(loc+"binned_z.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["bz", "frequency"])
    csvwriter.writerows(bz) 

#Write the magnitude data to a CSV
with open(loc+"binned_mag.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["b", "frequency"])
    csvwriter.writerows(b) 

print("Data scraped!")