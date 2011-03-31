# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def interp3D_01( u000,  u100,  u010,  u001,
                 u011,  u101,  u110,  u111,
                 x,  y,  z):
    """
    given u(0,0,0), u(1,0,0), ..., u(1,1,1)
    for any 0<x<1, 0<y<1, 0<z<1, 
    return u(x,y,z)
    
    algorithm 
      u ~= a+bx+cy+dz+eyz+fxz+gxy+hxyz

      a=u000; b=u100-u000; c=u010-u000; d=u001-u000;
      e=u011-a-c-d; f=u101-a-b-d; g=u110-a-b-c;
      h=u111-a-b-c-d-e-f-g;
      """

    a=u000; b=u100-u000; c=u010-u000; d=u001-u000;
    e=u011-a-c-d; f=u101-a-b-d; g=u110-a-b-c;
    h=u111-a-b-c-d-e-f-g;
    
    return a+b*x+c*y+d*z+e*y*z+f*x*z+g*x*y+h*x*y*z;


# version
__id__ = "$Id$"

# End of file 
