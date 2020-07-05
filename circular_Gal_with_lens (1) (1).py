# -*- coding: utf-8 -*-
"""
This program simulates weakly lensed galaxies by a simple isothermal sphere 
dark matter profile. The intrinsic ellipticities are generated with a Gaussian
distribution and the positions are generated randomly. After a lens in the
form of A/R is applied, the galaxies are cataloged onto and external file and
then illustrated in a figure window to demonstrate the effects of weak gravitational
lensing.

@author: William
"""

# Should be fairly obvious by now, just importing necessary modules.
from pylab import figure, show, rand, randint 
from numpy import array, empty, sqrt, arctan, rad2deg, deg2rad, pi, cos, sin, array_str, conjugate, angle
from matplotlib.patches import Ellipse
from numpy.random import normal  
from math import atan2
import random 



num_galaxies = 1000 # This will be how many galaxies are "found"
# in our patch of sky. Since we do not have actual data, I will use a random value.

print ("We have found " + str(num_galaxies) + " source galaxies.")

galaxy = [] # Empty list to fit however many galaxies we find
sgal = []

keeper = 0
counter = 0 # initiate the loop counter as one
index = 0 # initiate the nested loop counter as zero

# The following lines create the empty arrays for each parameter of a galaxy.
# We will save its x & y positions; its major & minor axes; and theta, the angle
# with respect to the x axis.
e1 = empty([num_galaxies,1], dtype ='cfloat') # Intrinsic Complex ellipticity
eg = empty([num_galaxies,1], dtype = 'cfloat') # Complex shear
ef1 = empty([num_galaxies,1], dtype = 'cfloat') # Final complex ellipticty
r = empty([num_galaxies, 1], dtype = 'f') # Magnitude of position vector.
g = empty([num_galaxies,1], dtype = 'f') # Magnitude of gamma, or shear effect
R = empty([num_galaxies,1], dtype = 'f') # R is the ratio between minor and major axes
R0 = empty([num_galaxies,1], dtype = 'f') # Axis ratio of intrinsic galaxy.
phi = empty([num_galaxies,1], dtype = 'f') # Position angle
major = empty([num_galaxies, 1], dtype = 'f') 
major0 = empty([num_galaxies, 1], dtype = 'f')
minor = empty([num_galaxies, 1], dtype = 'f')
minor0 = empty([num_galaxies, 1], dtype = 'f') 
theta = empty([num_galaxies, 1], dtype = 'f') # Final orientation
theta0 = empty([num_galaxies, 1], dtype = 'f') # Intrinsic orientation

# Start an empty array that holds two values.
xy = empty([1, 2])
position = [xy  for i in range(num_galaxies)] # Initiate a list of galaxies found,
# for now this is a list full of empty arrays.

# Creates a new file or replaces one that already exists. 
ff = open('telescope.txt', 'w+')

# This loop iterates once for each galaxy found
while counter < num_galaxies:
    # Pulling intrinsic ellipticities from Gaussian distribution.
    e1[counter] = complex(normal(0,.1,1), normal(0,.1,1))
    #e1[counter] = complex(0,0)

    # r here is the magnitude of the position vector from the origin.
    # Generate a random number with a minimum value of 3 and a maximum value of 10sqrt(2)
    # We want to exclude anything within a .5 Mparsecs of the source image. 
    #r[counter]= random.uniform(.5,2)
    
    # Generate a random angle from zero to 2pi. Phi is the POSITION angle on the
    # simulation grid..
    #phi[counter] = random.uniform(0,2*pi) 

    # Find the x and y positions using the polar coordinates from above.
    xy = array([random.uniform(-2,2), random.uniform(-2,2)])
    #xy = array([r[counter]*cos(2*phi[counter]), r[counter]*sin(2*phi[counter])])
    position[counter] = [xy] # Simply saves the position for database purposes.
    r[counter] = sqrt(xy[0]**2 + xy[1]**2)
    phi[counter] = atan2(xy[1],xy[0]) 
    # Magnitude of gamma.
    g[counter] = .35/float(r[counter])
    
    # This is the complex shear found using |g|exp(2*phi).
    eg[counter] = complex(-g[counter]*cos(2*phi[counter]), -g[counter]*sin(2*phi[counter]))

    #Now that we have both shear and source complex ellipticities, to get the final orientation
    #of the galaxy we simply add together the two complex numbers
 
    ef1[counter] = (e1[counter]+eg[counter])#/(1+conjugate(eg[counter])*e1[counter])
    
    # theta is the ellipse angle. This is here only for the purpose of the Ellipse
    # function used ahead and to make sure the shear is applied tangentially, not radially.
    theta[counter] = .5*angle(complex(ef1[counter].real, ef1[counter].imag), deg = 'true')
    theta0[counter] = .5*angle(complex(e1[counter].real, e1[counter].imag), deg = 'true')
        
    #Calculating the magnitude of the complex number modelling the ellipse
    mag = abs(ef1[counter])
    mag0 = abs(e1[counter])

    #This is the expression for how magnitude and axis ratio relate
    R[counter] = (1-mag)/(1+mag)
    R0[counter] = (1-mag0)/(1+mag0)
    #This generates the actual values for the axes, setting the major to some random
    #number from 1 to .1   
    a = rand(1)*.05  
    
    minor[counter] = a
    major[counter] = minor[counter]/R[counter]
    minor0[counter] = a
    major0[counter] = minor0[counter]/R0[counter]
    
    
    # Converts each of the elements to a string
    # s = array_str(xy[0]) + ","+array_str(xy[1])+","+array_str(ef1[counter][0].real)+","+array_str(ef1[counter][0].imag)+"\n"
    s = str(xy[0]) + "," + str(xy[1]) + "," + str(ef1[counter][0].real) + "," +  str(ef1[counter][0].imag)+"\n" 
    ff.write(s) # Write this to the file
    #print s # Print what is being written
    
    # sgal and galaxies are the source and lensed galaxies, respectively. These
    # lines create lists of the ellipse objects to plot.
    if mag <= .8:
        if r[counter] >= .5:
            sgal.append(Ellipse(xy, major0[counter], minor0[counter], theta0[counter]))
            galaxy.append(Ellipse(xy, major[counter], minor[counter], theta[counter]))
            keeper += 1
    counter += 1 # No infinite loops.

ff.close # 
print ("Acceptable galaxies: " + str(keeper) )
# Plot the locations of galaxies.
fig = figure()
# Adds the subplot of axes to the figure.
ax = fig.add_subplot(111, aspect='equal')
# This is the mass at the center causing the g-lensing.
mass = Ellipse(array([0,0]),.25,.25,0)
# For every element, e, in the list galaxy, iterate once.

# Plot the lensed galaxies    
for e in galaxy:
    # Add the current element to axis.
    ax.add_artist(e)
    ax.add_artist(mass)
    # Set the face and edgecolors.
    e.set_facecolor('white')
    e.set_edgecolor('blue')
    mass.set_facecolor('black')
    mass.set_edgecolor('black')
# Plot the source galaxies over the lensed ones.
for w in sgal:
    ax.add_artist(w)
    w.set_facecolor('white')
    w.set_edgecolor('red')

# Set maximum and minimum values for the x and y axes and their corresponding
# labels.
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xlabel('x (Mpc)')
ax.set_ylabel('y (Mpc)')

show()


