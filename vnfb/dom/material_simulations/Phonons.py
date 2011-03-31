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
from vsat.Phonons import Phonons

from vnfb.dom.AtomicStructure import StructureTable
# vnf holder
from ComputationResult import ComputationResult
#PhononDispersionTable = o2t(PhononDispersion, {'subclassFrom': ComputationResult})
PhononsTable = o2t(Phonons, {'subclassFrom': ComputationResult})
import dsaw.db
PhononsTable.addColumn(
    dsaw.db.reference(name='matter', table=StructureTable, backref='phonons')
    )
# status
#   'n': normal
#   'd': deleted
PhononsTable.addColumn(dsaw.db.varchar(name='status', length=1, default='n'))


PhononsTable.datafiles = [
    'DOS',
    'Omega2',
    'Polarizations',
    'Qgridinfo',
    'WeightedQ', # this is optional actually
    'data.idf/DOS',
    'data.idf/Omega2',
    'data.idf/Polarizations',
    'data.idf/Qgridinfo',
    ]


def readPickledPhonons(path, phonons):
    '''read phonons from pickled files and establish the phonon record

    phonons: a data object of Phonons (not a db record)

    assumptions:
      Qaxes: correpsonds to the reciprocal base "matter.lattice.recbase"

    polarizations and energies were saved in pickled files. Files:

    energies.pkl
    polarizations.pkl
    '''
    #
    import os, pickle, numpy
    load = numpy.load

    #
    energiesfile = os.path.join(path, 'energies.pkl')
    polarizationsfile = os.path.join(path, 'polarizations.pkl')

    energies = load(energiesfile)
    nx,ny,nz,nbr = energies.shape
    
    polarizations = load(polarizationsfile)
    ncube1,nbr1,natoms,dim = polarizations.shape

    # check
    assert ncube1 == nx*ny*nz
    assert nbr == nbr1
    assert nbr == natoms*dim

    # convert polarizations to idf-compatible format
    # pols = numpy.zeros((ncube1, nbr1, natoms, dim, 2))
    # pols[:, :, :, :, 0] = polarizations.real
    # pols[:, :, :, :, 1] = polarizations.imag
    # del polarizations
    phononsrecord.polarizations = polarizations
    phononsrecord.energies = energies

    # establish the database record
    #  nAtoms
    matter = phononsrecord.matter
    assert natoms == len(matter)
    phononsrecord.nAtoms = natoms

    #  dimension
    phononsrecord.dimension = dim

    #  Qaxes ???
    lattice = matter.lattice
    rbase = lattice.recbase
    Qaxes = [
        (rbase[0], nx),
        (rbase[1], ny),
        (rbase[2], nz),
        ]
    phononsrecord.Qaxes = Qaxes
    
    return phononsrecord


def computeDOS(phonons, N=10000):
    (b1,n1), (b2,n2), (b3,n3) = phonons.Qaxes
    nbr = phonons.nAtoms * phonons.dimension

    from random import random
    import numpy
    es = numpy.zeros(N*nbr)
    
    for i in range(N):
        x = random(); y = random(); z=random()
        Q = x*b1 + y*b2 + z*b3
        for j in range(nbr):
            es[i+j*N] = phonons.energy(Q, j)
            continue
        continue
    I, e = numpy.histogram(es, bins=100, range=(0, es.max()*1.2), new=True)
    return e,I



# version
__id__ = "$Id$"

# End of file 
