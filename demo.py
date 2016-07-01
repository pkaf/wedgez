import numpy as np
import numpy.random as rd

import wedge
reload(wedge)

# Generate some fake data
theta = rd.uniform( 110,120,500 )
radius= rd.uniform( 0,2,500 )
s     = rd.uniform( 5,50,500)

#Plot A: Simple example
ax1, aux_ax, pltinst, fig = wedge.cone(theta, radius, s,
                                       plotpos={'angle':2,
                                                'loc':[(theta.max()+theta.min())*0.5-90, 0.]},
                                       fig={'fignum':1, 'figsize':(4, 10)}, 
                                       scatter={'color':'g', 'marker':'o', 'alpha':0.5})

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




