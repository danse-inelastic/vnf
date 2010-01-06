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
        self.Qbasis = [q for q,n in Qaxes]
        self.polarizations = polarizations
        self.energies = energies

        self._toFractionalQ = self._toFractionalQMatrix()
        return


    def energy(self, Q=None, branch=0):
        fractional = self._fractionalQ(Q)
        return self._interpolate(fractional, self.energies[:,:,:,branch])


    def getDispersionCurve(self, Qstart, Qend, branch=0, npoints=10):
        Qstart = numpy.array(Qstart)
        Qend = numpy.array(Qend)
        Qstep = (Qend-Qstart)/(npoints-1)
        x = numpy.arange(0,1+1e-10,1./(npoints-1))
        y = map(lambda i: self.energy(Qstart+Qstep*i, branch), range(npoints))
        return x,y


    def getDispersionCurves(self, Qstart, Qend, branches=[0], npoints=10):
        Qstart = numpy.array(Qstart)
        Qend = numpy.array(Qend)
        Qstep = (Qend-Qstart)/(npoints-1)
        x = numpy.arange(0,1+1e-10,1./(npoints-1))
        ys = [ map(lambda i: self.energy(Qstart+Qstep*i, branch), range(npoints))
               for branch in branches ]
        return x,ys


    def getDispersionCurvesAsCombinedSegments(self, Qpoints, branches=[0], npointspersegment=10):
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


    def _toFractionalQMatrix(self):
        m = numpy.array(self.Qbasis)
        f = numpy.linalg.inv(m.T)
        return f
        


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
