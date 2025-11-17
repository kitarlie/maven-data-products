'''
Contains the following handy dandy maths tools:

    sign(x): returns the sign of a number x (+1 or -1)
    round_half_int(x): returns the half-integer closest to x
    vector_angle(a,b): returns the angle between vectors a and b in degrees
'''

from math import trunc
from numpy import acos, linalg, pi

def sign(x):
    '''
    Returns 1 if x>0, and -1 if x<0
    '''
    return x/abs(x)

def round_half_int(x):
    '''
    Returns the closest half-integer to the input x
    '''
    #Decimal part of the number
    y = (x - trunc(x))**2
    if y >= 0.75**2:
        return(trunc(x) + sign(x))
    elif y < 0.25**2:
        return(trunc(x))
    else:
        return(trunc(x) + 0.5*sign(x))
    

def vector_angle(a, b):
    '''
    Returns the angle between vectors a and b, in degrees
    a.b = abcos(theta)
    '''

    return 180/pi * acos((a[0]*b[0] + a[1]*b[1] + a[2]*b[2])/(linalg.norm(a)*linalg.norm(b)))
