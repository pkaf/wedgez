#########################################################################
# Makes RA/Dec-Redshift cone plot
#
#
#########################################################################

from __future__ import print_function, absolute_import, division

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
from mpl_toolkits.axisartist.floating_axes import FloatingSubplot
from mpl_toolkits.axisartist.floating_axes import GridHelperCurveLinear
from mpl_toolkits.axisartist import angle_helper
from mpl_toolkits.axisartist.grid_finder import MaxNLocator
from matplotlib.projections import PolarAxes

# try:
#     from cosmolopy import distance
# except ImportError:
#     lookbacktime = None

__all__ = ["cone"]


def cone(ra, z, scale=0.5, orientation='horizontal',
         raaxis='min', ralim=None, zlim=None, hms=False,
         # cosmology=None, lookbtime=False,
         plot=None, fig=None, subnum=None,
         xlabel=r"$\alpha$", ylabel=r"$\mathsf{redshift}$", **kwargs):

    """
    Make a wedge plot of RA/Dec vs redshift z, where RA/DEC are in degrees

    Parameters
    ----------
    Input data

    angle : (n, ) array
            RA in degrees
    redshift : (n, ) array

    scale: 0.5

    orientation:
        'horizontal': increasing z along +ve xaxis
        'vertical': increasing z along +ve yaxis
        angle in degrees: increasing z along the tilted axis

    raxis: 'min' | 'mid' | float
        default is 'min'
        RA value along which the cone plot is orientated horizontal
        or vertical

    ralim, zlim: list [ramin, rmax], list [zmin, zmax]
        default is taken from the lower/upper bound of the input data

    scatter: any kwargs compatible with plt.scatter

    hms: show RA labels in units of hours (if True) or degrees (if False)

    lookbtime: True/False

    plot: None
         'scatter' | 'hexbin' etc
    fig: supply figure instance
         default None

    subnum: subplot number e.g. 111, 221 etc
            default None

    xlabel: r"$\alpha$"

    ylabel: r"$\mathsf{redshift}$"

    cosmology: dict
     Uses cosmolopy package to compute look-back time
     default cosmology is {'omega_M_0': 0.3,
                           'omega_lambda_0': 0.7,
                          'h': 0.72}

    kwargs
    ------
    scatter = {'s': 4, 'marker': ','}

    Notes
    -----
        --Decorations that can be done outside the code:
             Draw grids: ax.grid(True, alpha=0.2)
             Set title: ax.set_title('Wedge plot')

        --Look-back time as twin axis to redshift not yet implemented

        --In future plan is to able to put colorbar in the plot too.
          Using cmap option.
    """

    # ------ Extents of ra and z
    if ralim:
        ramin, ramax = ralim
    else:
        ramin, ramax = ra.min(), ra.max()

    if zlim:
        zmin, zmax = zlim
    else:
        zmin, zmax = z.min(), z.max()

    # ----- Scale and Orientation of the wedge
    if orientation == 'horizontal':
        dirn = 0.
    elif orientation == 'vertical':
        dirn = 90.
    else:
        dirn = orientation

    if raaxis == 'min':
        raaxis = ramin
    elif raaxis == 'mid':
        raaxis = 0.5*(ramin+ramax)

    # Tilt of a cone relative to minimum RA
    tr_rotate = Affine2D().translate(dirn/scale - raaxis, 0.0)

    # Scaling the opening angle
    tr_scale = Affine2D().scale(scale*np.pi/180., 1.0)

    tr = tr_rotate + tr_scale + PolarAxes.PolarTransform()

    # ---- Grids
    if hms is True:
        grid_locator1 = angle_helper.LocatorHMS(4.0)
        tick_formatter1 = angle_helper.FormatterHMS()
    else:
        grid_locator1 = angle_helper.LocatorDMS(4.0)
        tick_formatter1 = angle_helper.FormatterDMS()

    grid_locator2 = MaxNLocator(10)

    grid_helper = GridHelperCurveLinear(tr,
                                        extremes=(ramin, ramax, zmin, zmax),
                                        grid_locator1=grid_locator1,
                                        grid_locator2=grid_locator2,
                                        tick_formatter1=tick_formatter1,
                                        tick_formatter2=None)

    # Figure properties
    if not fig:
        fig = plt.figure(figsize=(8, 7))
        subnum = 111
    ax = FloatingSubplot(fig, subnum, grid_helper=grid_helper)
    fig.add_subplot(ax)

    # adjust axis
    # Left, right, top represent z, lookbacktime, RA respectively.
    # right axes is for look-back time yet to be coded
    ax.axis["left"].set_axis_direction("bottom")

    ax.axis["right"].set_axis_direction("top")

    ax.axis["bottom"].set_visible(False)

    ax.axis["top"].set_axis_direction("bottom")
    ax.axis["top"].toggle(ticklabels=True, label=True)
    ax.axis["top"].major_ticklabels.set_axis_direction("top")
    ax.axis["top"].label.set_axis_direction("top")

    ax.axis["left"].label.set_text(ylabel)
    ax.axis["top"].label.set_text(xlabel)

    # create a parasite axes that transData in RA, z
    aux = ax.get_aux_axes(tr)
    aux.patch = ax.patch    # for aux_ax to have a clip path as in ax
    ax.patch.zorder = 0.9    # but this has a side effect that the patch is
    # drawn twice, and possibly over some other
    # artists. So, we decrease the zorder a bit to
    # prevent this.

    if plot == 'scatter':
        aux.scatter(ra, z, **kwargs)
        # plt.tight_layout()
        # plt.show()
    return ax, aux, fig
