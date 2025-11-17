'''
For checking whether Earth and Mars lie on the same Parker field line (or within a certain angle of the same field line).
'''

from astropy.time import Time
from astropy import units as u
from astropy.coordinates import get_body_barycentric, Angle
import numpy as np
from math import trunc

def time_string(daystring, i, i_max):
    '''
    Parameters:
        daystring (str): the date in format "YYYYMMDD" 
        i: the current index of the CDF file
        i_max: the final index of the CDF file 

    Returns:   
        The date and time in format "YYYY-MM-DD hh:mm"
    '''
    #Split daystring (YYYYMMDD) into year, month and day
    year = daystring[:4]
    month = daystring[4:6]
    day = daystring[6:]

    #Get time in HH:MM for the current index
    time = trunc(i/i_max * 24*60)
    minute = time % 60
    hour = str(int((time - minute)/60))
    minute = str(minute)

    #Ensures minute and hour have 2 digits each
    if len(minute) == 1:
        minute = "0" + minute
    if len(hour) == 1:
        hour = "0" + hour

    #Return date and time in form "YYYY-MM-DD hh:mm"
    return(year+"-"+month+"-"+day+" "+hour+":"+minute)



def is_mars_aligned(t, a):
    '''
    Inputs: t: the date and time
            a: the critical angle within which Earth and Mars are considered to be 'aligned' in the Parker spiral in radians
    '''

    print(t)

    t = Time(t)

    angle = Angle(a, unit = u.rad)
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
    
    if delta <= angle:
        return True
    else:
        return False