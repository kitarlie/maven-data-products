from math import trunc

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