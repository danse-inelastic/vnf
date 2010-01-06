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


from _ import o2t


# data object
class PhononDispersion(object):

    matter = None
    nAtoms = 1
    dimension = 3
    Qaxes = [[1,0,0], [0,1,0], [0,0,1]]
    polarizations = None # numpy array of nx * ny * nz * nD * nAtoms * nD *2  (the last 2 due to the vector is complex)
    energies = None # numpy array of nx * ny * nz * (nD*nAtoms)

    def __init__(self, matter=None, nAtoms=None, dimension=None, Qaxes=None, polarizations=None, energies=None):
        self.matter = matter
        self.nAtoms = nAtoms
        self.dimension = dimension
        self.Qaxes = Qaxes
        self.polarizations = polarizations
        self.energies = energies
        return


    def energy(self, Q=None, branch=0):
        fractional = self._fractionalQ(Q)
        return self._interpolate(fractional, self.energies[:,:,:,branch])


    def getDispersionCurve(self, Qstart, Qend, branch=0, npoints=20):
        Qstart = numpy.array(Qstart)
        Qend = numpy.array(Qend)
        Qstep = (Qend-Qstart)/(npoints-1)
        x = numpy.arange(0,1+1e-10,1./(npoints-1))
        y = map(lambda i: self.energy(Qstart+Qstep*i, branch), range(npoints))
        return x,y


    def getDispersionCurves(self, Qstart, Qend, branches=[0], npoints=20):
        '''get dispersion curves from Qstart to Qend for the given branches'''
        Qstart = numpy.array(Qstart)
        Qend = numpy.array(Qend)
        Qstep = (Qend-Qstart)/(npoints-1)
        x = numpy.arange(0,1+1e-10,1./(npoints-1))
        ys = [ map(lambda i: self.energy(Qstart+Qstep*i, branch), range(npoints))
               for branch in branches ]
        return x,ys


    def getDispersionPlot(self, Qpoints, branches=[0], npointspersegment=20):
        '''get dispersion plot for the given branches

        The plot is the typical dispersion plot that has several curves; one
        curve for one branch.
        Each curve has several segments. Each segment start from Qpoints[i], and
        ends with Qpoints[i+1].
        '''
        x = []
        ys = [[] for b in branches]
        for i,(Qstart, Qend) in enumerate(zip(Qpoints[:-1], Qpoints[1:])):
            x1, ys1= self.getDispersionCurves(
                Qstart, Qend, branches=branches, npoints=npointspersegment)
            x1 += i
            x = numpy.concatenate((x, x1))
            for j, y in enumerate(ys):
                ys[j]=numpy.concatenate((y,ys1[j]))
                continue
            continue
        return x, ys


    def getDefaultDispersionPlot(self, branches=None, npointspersegment=20):
        if branches is None:
            branches = range(self.dimension*self.nAtoms)
            
        matter = self.matter
        sg = matter.sg
        from math import pi
        
        if sg.number == 225: # fcc
            a = matter.lattice.a
            b = 2*pi/a
            Qpoints = [
                (0,0,0),
                (0,0,b),
                (0,b,b),
                (0,0,0),
                (b/2,b/2,b/2),
                ]
            
        elif sg.number == 229: # bcc
            a = matter.lattice.a
            b = 2*pi/a
            Qpoints = [
                (b/2,b/2,0),
                (0,0,0),
                (b,0,0),
                (b/2,b/2,b/2),
                (0,0,0),
                ]
            
        else:
            raise NotImplementedError

        return self.getDispersionPlot(Qpoints, branches, npointspersegment)


    def _fractionalQ(self, Q):
        return numpy.mod(numpy.dot(self._toFractionalQ, Q), 1)


    def _interpolate(self, x, fm):
        shape = fm.shape
        scale = numpy.array(shape)-1
        x1 = x*scale
        f, m = numpy.modf(x1)
        m = numpy.array(m, int)

        if self.dimension != 3: raise NotImplementedError
        mx, my, mz = m
        us = [fm[mx,my,mz], fm[mx+1,my,mz], fm[mx,my+1,mz], fm[mx,my,mz+1],
             fm[mx,my+1,mz+1], fm[mx+1,my,mz+1], fm[mx+1,my+1,mz], fm[mx+1,my+1,mz+1],
             ]
        args = us + list(f)
        from vnfb.utils.math import interp3D_01
        return interp3D_01(*args)


    def _getQbasis(self):
        return [q for q,n in self.Qaxes]
    Qbasis = property(_getQbasis)


    def _createToFractionalQMatrix(self):
        m = numpy.array(self.Qbasis)
        f = numpy.linalg.inv(m.T)
        return f
    def _getToFractionalQ(self):
        k = '_toFractionalQ_'
        if hasattr(self, k): return getattr(self, k)
        v = self._createToFractionalQMatrix()
        setattr(self, k, v)
        return v
    _toFractionalQ = property(_getToFractionalQ)


import numpy
        
                                 


# orm
from vnfb.dom.AtomicStructure import Structure

from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    matter = InvBase.d.reference(
        name='matter', targettype=None, targettypes=[Structure], owned=0)

    dbtablename = 'phonondispersions'

PhononDispersion.Inventory = Inventory
del Inventory


# db table
from ComputationResult import ComputationResult
PhononDispersionTable = o2t(PhononDispersion, {'subclassFrom': ComputationResult})
PhononDispersionTable.datafiles = [
    'DOS',
    'Omega2',
    'Polarizations',
    'Qgridinfo',
    'WeightedQ', # this is optional actually
    ]



# version
__id__ = "$Id$"

# End of file 
