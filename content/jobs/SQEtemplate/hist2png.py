
import os
from histogram.plotter import defaultPlotter as p
import matplotlib
matplotlib.use( 'ps' )
import pylab


def hist2png( h, filename = None ):
    p.plot( h )
    if filename is None: filename = h.name()
    ps = '%s.ps' % filename 
    png = '%s.png' % filename 
    pylab.savefig( ps )
    os.system( 'convert %s %s' % (ps, png) )
    return png
