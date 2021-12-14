# GravitySimulation
Some simple methods for calculating Newtonian gravity.

This uses a crude n-body (O(n^2)) simulation and is designed for bound systems.
Any set of bodies can be used by following the basicSolarSystem function in SystemLibrary.py and changing the target function in RunSystem.py.
RunSystem.py can output the results as a series of .pngs (frequency of imgs can be modified) or as a set of n .txt files containing the mass, location, velocity and time(s) for each timestep. Note that for these to work the relevent directories must be created. 
Finally the data from the .txt files can be used to create an animation.

Dependencies: matplotlib, astropy, numpy, operator, concurrent.futures
