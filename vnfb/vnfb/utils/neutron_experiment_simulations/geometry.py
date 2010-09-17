# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import numpy as np
from mcni.neutron_coordinates_transformers import mcstasRotations
def tomatrix(orientation):
    ''' convert orientation to matrix representation

    if the input is a 3-tuple, it is assumed to be rotation angles
    in degrees (3 consecutive rotations along x,y,z axis)

    if the input can be reshaped to 3X3 matrix, just reshape it and return
    '''
    orientation = np.array(orientation)
    if orientation.size==3:
        return mcstasRotations.toMatrix(*orientation)
    elif orientation.size==9:
        orientation.shape =3,3
        return orientation
    raise ValueError, str(orientation)


def toangles(orientation):
    '''convert orientation to 3 consecutive rotations (in degrees) along
    x,y,z axes

    if the input is a 3x3 matrix, it is assumed to be the rotation matrix

    if the input is a 3-tuple like object, just return it

    return: a 3-tuple
    '''
    if orientation is None:
        return 0,0,0
    orientation = np.array(orientation)
    if orientation.size==3:
        pass
    elif orientation.size==9:
        orientation.shape = 3,3
        orientation = mcstasRotations.toAngles(orientation, unit='degree')
    else:
        raise ValueError, str(orientation)
    return tuple(orientation)


def calculateAbsoluteCoordinates(relative_coordinates):
    '''calculate the "absolute coordindates" of elements out of the "relative coordinates"

    The so-called "relative coordinates" are used to describe the geometrical
    interrelation of the elements. For example

     "guide2":  "guide1", [0,0,3], [[1,0,0], [0,0,1], [0,-1,0]] 

    means that guide2 is z=3 relative to guide1, and rotated 90 degrees along x axis.

    The format of a relative_coordinate is

      element: reference_element, position, orientation

    where position is a vector, and orientation is a 3X3 matrix.

    When reference_element is not specified, the entry is an absolute coordinate.

    There must be at least one entry in relative_coordinates that is "absolute".

    The whole set of relative_coordinates specification must be complete enough
    to resolve the absolute coordinates of all elements.
    '''
    class _solver:

        def __init__(self):
            # container of absolte coords
            self.result = {}
            return

        def solve(self, relative_coordinates):
            self.relative_coordinates = relative_coordinates
            for element in relative_coordinates:
                if element in self.result:
                    continue
                self.result[element] = self._resolve(element)
                continue
            return self.result

        def _resolve(self, element):
            reference, position, orientation = self.relative_coordinates[element]
            orientation = tomatrix(orientation)
            if not reference:
                self.result[element] = position, orientation
                return position, orientation
            refabspos, refabsorientation = self._resolve(reference)
            abspos = refabspos + np.dot(refabsorientation.T, position)
            absorientation = np.dot(orientation, refabsorientation)
            r = self.result[element] = abspos, absorientation
            return r
        
    return _solver().solve(relative_coordinates)



import numpy
I = numpy.array(
    [[1,0,0],
     [0,1,0],
     [0,0,1],
     ])
def calculateComponentAbsoluteCoordinates(components, getname=None):
    """calculate the absolute coordinates of all components.

    The given components might have relative coords. This method
    calculates the absolute coordinates and assign that back to
    the components.

    All components must be instances of vnfb.dom.neutron_experiment_simulations.AbstractNeutronComponent or vnfb.dom.neutron_experiment_simulations.Scatterer

    getname: method to get name attribute of a component.
        when the components are instances of AbstractNeutronComponent, use default
        when the components are scatterers (instances of Scatterer), use a method to return scatterer.scatterername
    """
    if not getname:
        getname = lambda c: c.componentname

    # prepare to call calculateAbsoluteCoordinates
    componentdict = {}
    relative_coords = {}
    for c in components:
        name = getname(c)
        componentdict[name] = c
        
        # c is a db record. c.position and c.orientation both could be None
        pos = c.position
        if pos is None: pos = (0,0,0)
        ori = c.orientation
        if ori is None: ori = I

        #
        relative_coords[name] = c.referencename, pos, ori
        continue

    # call calculateAbsoluteCoordinates
    abscoords = calculateAbsoluteCoordinates(relative_coords)

    # assign coords back to component
    for name, (pos, ori) in abscoords.iteritems():
        c = componentdict[name]
        c.referencename = ''
        c.position = pos
        c.orientation = ori
        continue
    return components


# version
__id__ = "$Id$"

# End of file 
