# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 20:46:32 2015

@author: William
"""
from numpy import array, empty, sqrt 
import matplotlib.pyplot as plot
from scipy.optimize import leastsq as lsq
from numpy.random import normal
from numpy import mean as avg
from matplotlib import pyplot as plt



""" 2015 - Py 2
# Open the telescope file, read only. That way if we get any true data
# from a telescope, we won't mess it up.
ff = open('telescope.txt', 'r')
# Go through every line in the file. It will split the values at the commas and
# Make it an element of this list. 
c= [map(float,line.split(',')) for line in ff ]

#print c # This is trivial.
size = len(c)
2020"""



def rf(x1,y1):
    return sqrt(x1**2+y1**2)
    
def gf(a,r1):
    return a/r1
# b is the parameter vector, r1 is the dependent variable, y is a theoretical value
def err(b,y,r1):
    v1 = b
    return v1/r1 - y # this defines the error, the estimated guess minus the theoretical value.
# Serves to evaluate our function using the fitted parameters
def peval(r1, b):
    return b[0]/r1

""" 2015 -- Code was written for Py 2
# Create empty arrays with placeholders for each value obtained from the file.
x=empty(size); y = empty(size); e1= empty(size); e2 = empty(size); ei = empty(size, dtype = 'cfloat')
# These are empty arrays with placeholders for information calculated.
r = empty(size, dtype = 'float'); g = empty(size, dtype = 'cfloat'); ef=empty(size, dtype = 'cfloat')
"""
# 2020 -- Coordinates
x = []; y = []
# 2020 -- Ellipticties
e1 = []; e2 = []; ei = []
# 2020 -- Mathmatics
r = []; g =[]; ef = []

countlines = 0
# Open file and read each line as well as the data
# within and add to the empty lists.
with open('telescope.txt', 'r') as ff:
    for line in ff:
        c = line.split(",")
        x.append(float(c[0]))
        y.append(float(c[1]))
        r.append(rf(x[countlines],y[countlines]))
        e1.append(float(c[2]))
        e2.append(float(c[3]))
        ef.append(complex(e1[countlines], e2[countlines]))
        efmag = abs(ef[countlines])
        efmag = 1-efmag/(1+efmag)
        g.append(ef[countlines])
        countlines +=1        


""" 2015 -- Py 2
ff.close() # This is obvious.
# Every ith element here is a particular galaxy. 
for i in range(0,size):
    x[i] = c[i][0] # Save the first element of the ith galaxy
    y[i] = c[i][1] # Save the second element of the ith galaxy
    r[i] = rf(x[i],y[i])
    e1[i] = c[i][2] # Save the third element of the ith galaxy
    e2[i] = c[i][3] # Save the fourth element of the ith galaxy
    ef[i] = complex(e1[i], e2[i])
    efmag = abs(ef[i])
    axratio = 1-efmag/(1+efmag) # Maybe this is useful? The ratio of minor/major axis.
    g[i] = ef[i] # Are we supposed to assume the shear is approximately equal to the total ellipticity?
2020
""" 

# "Donut" is a visualization of a bin that contains certain data points within
# a given inner and outer radius. 
donut1 = []; donut2 = []; donut3 = []; donut4 = []; donut5 = [];
donut6 = []; donut7 = []; donut8 = []; donut9 = []; donut10 = []; donut11 = [];

# For every element, e, in r, iterate
k = 0
for e in r:
    # If the radius e found in r is within a certain threshold, add it to its corresponding shear
    # to that list
    if .5 < e <= .7: # Each conditional statement is a different bin. 
        donut1.append(abs(g[k])) # Add this gamma value to the first list.
    elif .7 < e <= .9:
        donut2.append(abs(g[k])) # Add this gamma value to second ist
    elif .9 < e <= 1.1:
        donut3.append(abs(g[k])) # And so on..
    elif 1.1 < e <= 1.3:
        donut4.append(abs(g[k]))
    elif 1.3 < e <= 1.5:
        donut5.append(abs(g[k]))
    elif 1.5 < e <= 1.7:
        donut6.append(abs(g[k]))
    elif 1.7 < e <= 1.9:
        donut7.append(abs(g[k]))
    elif 1.9 < e:
        donut8.append(abs(g[k]))
    k += 1# Indexing purposes
"""    elif 11 < e <= 12:
        donut9.append(abs(g[k]))
    elif 12 < e <= 13:
        donut10.append(abs(g[k]))
    elif 13 < e <= 14:
        donut11.append(abs(g[k]))"""
    
# Take the average gamma for every bin.
g1 = avg(donut1); g2 = avg(donut2); g3 = avg(donut3); g4 = avg(donut4); g5 = avg(donut5)
g6 = avg(donut6); g7 = avg(donut7); g8 = avg(donut8); """g9 = avg(donut9); g10 = avg(donut10)
g11 = avg(donut11)"""
glist = [g1,g2,g3,g4,g5,g6,g7,g8] # Simply makes a list of all the averages.

# An arbitrary list for the scale of the radius. according to every bin.
rlist = [.6,.8,1,1.2,1.4,1.6,1.8,2]

# Create gtrue, expected true value of gamma.
gtrue = []
for z in rlist:
    gtrue.append(gf(.35,z))


 
p0 = [.5] # initial parameter guess
        
# This is an attempt to fit the data using the perceived function gf. p0 is the initial guess
# and the first argument in err. args will consist of any other arguments that might be necessary
# in the gf function.
        
fit = lsq(err, p0, args=(glist, rlist))
print (fit[0])

# Plotting stuff

"""ax = plot.figure().add_subplot(1,1,1)

for w in 
ax.plot([4,6, 8, 9.5],glist, 'bo',)
ax.set_xlabel('Distance from Mass r (Megaparsec)')
ax.set_ylabel('Shear')
ax.set_xlim(0, 10)
ax.set_ylim(0, 25)
"""
plt.plot(rlist, glist, 'ro', rlist, peval(rlist, fit[0]),rlist, gtrue)
plt.legend(['Measured', 'Least Squares Fit', 'True'])
plt.title('Singular Isothermal Sphere \n Least-squares fit to Measured Shear')
plt.ylabel('Shear')
plt.xlabel('Distance from Cluster')
plt.show()

