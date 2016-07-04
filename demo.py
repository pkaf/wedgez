import numpy as np
import numpy.random as rd
import wedge
import matplotlib.pyplot as plt
reload(wedge)

rd.seed(5)

# -------
# Example I
# -------

fig = plt.figure(1, figsize=(8, 6))
fig.subplots_adjust(wspace=0.3, left=0.05, right=0.95)

# Plot A: Simple example- Vertical orientation
theta = (8 + np.random.rand(100)*(14 - 8))*15.  # in degrees
radius = np.random.rand(100)*0.9

ax1, aux1, fig1 = wedge.cone(theta, radius, scale=0.2,
                             orientation='vertical', raaxis='min',
                             ralim=None, zlim=[0.01, radius.max()],
                             hms=False, plot='scatter', fig=fig, subnum=221,
                             **{'s': 10, 'marker': 'o', 'c': 'r'})
ax1.grid(True, alpha=0.2)

# Plot B: Simple example - Horizontal orientation
ax2, aux2, _ = wedge.cone(theta, radius, scale=0.2,
                          orientation='horizontal', raaxis=165.0,
                          ralim=None, zlim=[0.01, radius.max()],
                          hms=True, plot='scatter', fig=fig, subnum=222,
                          xlabel='RA', ylabel=r'$z$',
                          **{'s': rd.uniform(1, 100, theta.shape),
                             'marker': 'o', 'c': 'r', 'alpha': 0.2})

# -----------
# Example II
# 2dFGRS type example - Horizontal orientation
# -----------

fig = plt.figure(2, figsize=(7, 2))

phi1 = (8 + np.random.rand(100)*(14 - 8))*15.  # in degrees
phi2 = -(8 + np.random.rand(100)*(14 - 8))*15.  # in degrees

# Subplot in the left side
ax22, aux, _ = wedge.cone(phi2, radius, scale=0.25,
                          orientation=180, raaxis='mid',
                          ralim=[-210, -100], zlim=[0.01, radius.max()],
                          hms=True, plot='scatter', fig=fig, subnum=121,
                          xlabel='RA', ylabel=r'$z$',
                          **{'s': 15, 'marker': 'o', 'c': 'g'})
ax22.axis["left"].toggle(all=True)
ax22.axis["left"].major_ticklabels.set_axis_direction("top")

# Subplot in the right side
ax11, aux, _ = wedge.cone(phi1, radius, scale=0.25,
                          orientation='horizontal', raaxis='mid',
                          ralim=[100, 210], zlim=[0.01, radius.max()],
                          hms=True, plot='scatter', fig=fig, subnum=122,
                          xlabel='RA', ylabel=r'$z$',
                          **{'s': 15, 'marker': 'o', 'c': 'g'})

# plt.tight_layout()
fig.suptitle('2dFGRS type example')
plt.tight_layout()
fig.subplots_adjust(wspace=0.0001)

# -------
# Example III
# Hexbin
# -------

figIII = plt.figure(3, figsize=(8, 4))
figIII.subplots_adjust(wspace=0.3, left=0.05, right=0.95)

theta = (8 + np.random.rand(10000)*(14 - 8))*15.  # in degrees
radius = np.random.rand(10000)*0.9

ax31, aux31, figIII = wedge.cone(theta, radius, scale=0.5,
                                 orientation='horizontal', raaxis='mid',
                                 ralim=None, zlim=[0.001, radius.max()],
                                 hms=True, plot=None, fig=figIII, subnum=111)

h2d, _, _ = np.histogram2d(theta, radius)
aux31.imshow(h2d)
figIII.show()
# plt.tight_layout()
fig.savefig('demo.png', transparent=True)
