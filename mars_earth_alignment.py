'''
For checking whether Earth and Mars lie on the same Parker field line (or within a certain angle of the same field line).
'''

from astropy.time import Time
from datetime import date, timedelta
from astropy import units as u
from astropy.coordinates import get_body_barycentric, Angle
import numpy as np
import csv

def time_string(year, day):
    '''
    Parameters:
        daystring (str): the date in format "YYYYMMDD" 
        i: the current index of the CDF file
        i_max: the final index of the CDF file 

    Returns:   
        The date and time in format "YYYY-MM-DD hh:mm"
    '''
    #Day 1 of the year
    strt_date = date(int(year), 1, 1)

    #Convert to date
    res_date = strt_date + timedelta(days=int(day) - 1)
    res = res_date.strftime("%Y-%m-%d")

    #Return date and time in form "YYYY-MM-DD hh:mm"
    return(res + " 00:00")



def is_mars_aligned(t):
    '''
    Inputs: t: the date and time
    Returns: delta: the angle (in degrees) between the Parker spiral field lines associated with Earth and Mars, extrapolated back to the Earth's orbit.
    '''

    t = Time(t)

    half_turn = Angle(np.pi, unit = u.rad)
    full_turn = Angle(2*np.pi, unit = u.rad)

    #Heliocentric coordinates of Mars and Earth
    mars = (get_body_barycentric('mars', t) - get_body_barycentric('sun', t))
    earth = (get_body_barycentric('earth', t) - get_body_barycentric('sun', t))

    mars_r = mars.norm()
    earth_r = earth.norm()
    
    #The angle relative to the x-axis of the IMF field line connecting the Sun to Mars, at Earth's orbit
    mars_t = (earth_r/mars_r)*np.arctan2(mars.y, mars.x)

    #The angle relative to the x-axis of the IMF field line connecting the Sun to Earth, at Earth's orbit
    earth_t = np.arctan2(earth.y, earth.x)

    #Difference between angles
    delta = earth_t - mars_t

    #### Angle handling ####

    #Makes all angles positive (i.e. changes direction of negative angle separation)
    if delta < 0:
        delta = -delta

    #Changes reflex angle to complementary acute/obtuse angle
    if delta > half_turn:
        delta = full_turn - delta

    #Extract numerical value
    delta = delta.to_string()
    delta = delta.split(' ')
    delta = float(delta[0])
    
    return delta*180/np.pi

with open("C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/conjunction-angles.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Year", "Day", "Conjunction angle"])
    for year in range(1981, 2024):
        for day in range(1, 367):
            time = time_string(year, day)
            delta = is_mars_aligned(time)
            csvwriter.writerow([year, day, delta])