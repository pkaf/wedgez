import numpy as np
import numpy.random as rd
import wedge
reload(wedge)
import matplotlib.pyplot as plt

theta = (8 + np.random.rand(100)*(14 - 8))*15.  # in degrees
radius = np.random.rand(100)*2

#Plot A: Simple example

fig = plt.figure(1, figsize=(8, 4))
#fig.subplots_adjust(wspace=0.3, left=0.05, right=0.95)

ax, aux, fig = wedge.cone(theta, radius, scale=0.2, s=3, orientation='horizontal',
                          ralim=None, zlim=[0.01, radius.max()],
                          hms=False, fig=fig, subnum=111)

#fig.gca().annotate("A demo wedge plot")

#Plot B: Example with subplots
"""
cone_plot( theta, radius, 
plotpos={'angle':2, 'loc':[135-90,0.]}, 
fig={'fignum':2, 'subplot':311, 'figsize':(10,8)}, 
scatter={'color':'g', 'marker':'o', 'alpha':0.5})

cone_plot( theta, radius, 
plotpos={'angle':2, 'loc':[135-90,0.]}, 
fig={'fignum':2, 'subplot':312, 'figsize':(10,8)}, 
scatter={'color':'r', 'marker':'o', 'alpha':0.5})

cone_plot( theta, radius, 
plotpos={'angle':2, 'loc':[135-90,0.]}, 
fig={'fignum':2, 'subplot':313, 'figsize':(10,8)}, 
scatter={'color':'g', 'marker':'o', 'alpha':0.5})

"""




