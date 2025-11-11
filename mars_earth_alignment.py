from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import get_body_barycentric
import numpy as np

def is_mars_aligned(t, angle):
    '''
    Inputs: t: the date and time
            angle: the critical angle within which Earth and Mars are considered to be 'aligned' in the Parker spiral in radians
    '''

    #Heliocentric coordinates of Mars and Earth
    mars = get_body_barycentric('mars', t) - get_body_barycentric('sun', t)
    earth = get_body_barycentric('earth', t) - get_body_barycentric('sun', t)

    mars_r = np.linalg.norm(mars)
    earth_r = np.linalg.norm(earth)

    mars_t = np.arctan2(mars[1], mars[0])
    earth_t = np.arctan2(earth[1], earth[0])

    if earth_t - (earth_r/mars_r)*mars_t < angle:
        return True
    else:
        return False
