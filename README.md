# Dark-Matter-Singular-Isothermal-sphere
Simulating dark matter weak gravitational lensing due singular isothermal sphere (SIS) model.

This program was one of the tools I used for my undergraduate research (2014-2015) in cosmology and 
extragalactic astrophysics. The goal of the project was to simulate a survey of galaxies from a 
fictional telescope, apply a distortion effect on those images, save each unique galaxy to a file, 
and plot a 2D visualization of the images (source and distorted) on a cartesian grid. 

The second program is the least squares fit. The program attempts to extract data from the text file
created and analyzes it using a least squares method to find the shear value. From that value, a
dark matter profile can be deduced.

### SIMULATION OF DATA ###

The positions of the galaxies were randomly generated, since this was fictional data.
A Gaussian distribution surrounding 0 was used to generate the ellipticities for 
the source galaxies.

### DISTORTION ###

For the Singular Isothermal Sphere, the distortion effect was mathematically straightforward.
The distortion (depicted in blue) on the plot was tangential, as expected. 


### WRITING TO FILE ###

Each galaxy's x, y, major axis, and minor axis is recorded into a text file with each value
delimited by commas.

### PLOTTING ###

Each galaxy is plotted. The image does not include galaxies with distances too close to the SIS model.
Galaxies very close to the gravitational mass not be considered to be weakly lensed, but strongly lensed, 
which was beyond the scope of the project.

