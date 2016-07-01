#########################################################################
# Makes RA/Dec-Redshift cone plot
#
#
#########################################################################

from __future__ import print_function, absolute_import, division

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
from mpl_toolkits.axisartist.floating_axes import FloatingSubplot, GridHelperCurveLinear
from mpl_toolkits.axisartist import angle_helper
from matplotlib.projections import PolarAxes

__all__ = ["cone"]

def cone( *args, **kwargs ):
    """
    INPUT:
	args = a. RA in degrees and redshift z
               b. DEC in degrees and redshift z
	       c. RA/DEC, z and marker size 's' for a scatter plot
    kwargs
	     #tilt and angular width of plot
         plotpos  ={'loc':[ (ramin+ramax)/2, zmin], 'angle':1 }
                    
               'loc'[0]: For near vertical cone (erect or inverted)
                      this must be set to midpoint of ra (RAmid).
                      For horizontal cone RAmid - 90
                      For vertical cone RAmid - 180 etc. [Default]
               'loc'[1]: zmin = 0. #i.e. starts from z=0
                         If zmin = 1. vertical axis starts at z=1                        
               However, if 'angle':2 then 'loc'[0] angle has to be adjusted instead of substracting 90, 180 we have to substract 45, 135 so on so forth in order to get erect/invert plot
              
	     ralim    = from args| [ramin,rmax] 	
	     zlim     = from args| [zmin ,zmax] 	
             scatter  = any kwargs compatible with plt.scatter

	#Figure properties
	fig = { 'fignum':1, 'figsize': (4,10)}

    BUGS/FUTURE IMPROVEMENT:
        RA labels in HMS or DMS has to be set up manually.

        Still needs to be hand tweaked to adjust the tilt of the cone in the figure.

        Axis handling can be improved

        Can provide colorbar in the plot too. Using cmap option.            
    """
        
    #++++++++Args+++++++++++++
    if len(args)==2:    
        ra, z = args
        s = 4 
    elif len(args)==3:
        ra, z, s = args    
    #++++++++Args+++++++++++++


    ramin, ramax = ra.min(), ra.max()
    zmin , zmax  = z.min(),  z.max()

    #++++++++Cone: scale, orientation+++++++++++++
    if kwargs.has_key('plotpos')==True:
	if kwargs['plotpos'].has_key('loc')==False:
		kwargs['plotpos']['loc']=[ 0.5*(ramax+ramin)- 180., 0.]
	if kwargs['plotpos'].has_key('angle')==False:
		kwargs['plotpos']['angle']=2.
    else:
    	kwargs['plotpos'] = {'loc':[0.5*(ramax+ramin)-45., 0], 'angle':2}

    # Tilt of a cone
    tr_rotate = Affine2D().translate( kwargs['plotpos']['loc'][0], kwargs['plotpos']['loc'][1])

    # scale degree to radians
    tr_scale = Affine2D().scale((np.pi/180.)*kwargs['plotpos']['angle'], 1.)

    tr = tr_rotate + tr_scale + PolarAxes.PolarTransform() 
    #++++++++Cone: scale, orientation+++++++++++++


    #grid_locator1 = angle_helper.LocatorHMS(4.0)
    #tick_formatter1 = angle_helper.FormatterHMS()
    grid_locator1 = angle_helper.LocatorDMS(4.0)
    tick_formatter1 = angle_helper.FormatterDMS()

    from mpl_toolkits.axisartist.grid_finder import MaxNLocator
    grid_locator2 = MaxNLocator(10)

    #import pdb	
    #pdb.set_trace()
	
    #+++++++++++ set xlim,ylim++++++++++
    if kwargs.has_key('ralim')==False:
        ra0, ra1 = ramin, ramax	
    else:
        ra0, ra1 = kwargs['ralim'][0], kwargs['ralim'][1]	

    # set the limit of redshift
    if kwargs.has_key('zlim')==False:
        z0, z1 = zmin, zmax	
    else:
        z0, z1 = kwargs['zlim'][0], kwargs['zlim'][1]	
    #+++++++++++ set xlim++++++++++++++

    grid_helper = GridHelperCurveLinear(tr, extremes=(ra1, ra0, z1, z0),
                                        grid_locator1=grid_locator1,
                                        grid_locator2=grid_locator2,
                                        tick_formatter1=tick_formatter1,
                                        tick_formatter2=None)

    #++++++++++++ Figure properties++++
    if kwargs.has_key('fig')==False:
	kwargs['fig'] = {}
	kwargs['fig']['fignum']=1 
        kwargs['fig']['figsize']= (4,10)
    else:
        if kwargs['fig'].has_key('figsize')==False:
            kwargs['fig']['figsize'] = (4,10)
        if kwargs['fig'].has_key('fignum')==False:
            kwargs['fig']['fignum'] = 1
        if kwargs['fig'].has_key('subplot')==False:
            kwargs['fig']['subplot'] = 111

    #++++++++++++ Figure properties++++
    fig = plt.figure( kwargs['fig']['fignum'], 
                      figsize=kwargs['fig']['figsize'])
    ax1 = FloatingSubplot( fig, 111,#kwargs['fig']['subplot'],            
                               grid_helper=grid_helper)
    fig.add_subplot(ax1)


    #+++++++++++++ Axis plot++++++++++++

    # adjust axis
    ax1.axis["left"].toggle(ticklabels=False)

    ax1.axis["right"].toggle(ticklabels=True)
    ax1.axis["right"].set_axis_direction("bottom")
    ax1.axis["right"].label.set_visible(True)
    #ax1.axis["right"].major_ticklabels.set_pad(10) #label.set_visible(True)
    ax1.axis["right"].label.set_text(r"Redshift (z)")
    ax1.axis["right"].label.set_size(18)

    ax1.axis["bottom"].major_ticklabels.set_axis_direction("top")
    ax1.axis["bottom"].label.set_axis_direction("top")
    ax1.axis["bottom"].label.set_text(r"$\alpha_{2000}$")
    ax1.axis["bottom"].label.set_size(18)

    ax1.axis["top"].set_visible(False)

    # create a parasite axes whose transData in RA, z
    aux_ax = ax1.get_aux_axes(tr)

    aux_ax.patch = ax1.patch # for aux_ax to have a clip path as in ax
    ax1.patch.zorder=0.9 # but this has a side effect that the patch is
                        # drawn twice, and possibly over some other
                        # artists. So, we decrease the zorder a bit to
                        # prevent this.
    #+++++++++++++ Axis plot++++++++++++

    if kwargs.has_key('scatter'):
        scatter = kwargs['scatter']
    else:
        scatter = {}            

    pltinst = aux_ax.scatter(ra, z, s, **scatter )
    plt.show()
    return ax1, aux_ax, pltinst, fig

