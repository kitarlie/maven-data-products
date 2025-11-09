# maven-data-products
Code to create and use data custom data products using MAVEN data in CDF format, for my PHYS450 fourth year project. I will try and update this concurrently with my work, but I cannot guarantee that the version available here is exactly the same as the version that I am using. Note that I use an env file to store the locations of the MAVEN CDF files (which points to the Lancs LUNA data server) and the intended location of the binned data. 

**/legacy**: contains pre-repo legacy code in its latest version before the initial commit.

**b_field_histogram.py**: creates a plot similar to figure 2 from Brain et al. (2003) 'Martian magnetic morphology: Contributions from the solar wind and crust' from the summarised data in CSV format.

**bow_shock_model.py**: handles generation of, and comparisons to, a conic section model of the Martian bow shock as described in Hall et al. (2016) 'Annual variations in the Martian bow shock location as observed by the Mars Express mission'

**data_scraping.py**: takes stored MAVEN data files (in .cdf format) and summarises the x-, y- and z-components of the IMF (magnetometer measurements when MAVEN is outside the bow shock), as well as the magnitude, in frequency bins with resolution 0.1 nT.

**data_scraping_bxby.py**: takes stored MAVEN data files (in .cdf format) and summarises as a 2D matrix containing the frequency of occurrence of x- and y- components of the IMF between -20 nT and 20 nT, with resolution 1 nT.

**math_tools.py**: contains some handy dandy tools for returning the sign of a number and rounding numbers to the nearest half-integer.
