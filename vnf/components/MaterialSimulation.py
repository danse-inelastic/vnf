# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Engine:

    def __init__(self, id, short_description, long_description, nickname = ''):
        self.id = id
        self.short_description = short_description
        self.long_description = long_description
        self.nickname = nickname
        return
    

basic_engines = {
    'gulp': Engine('gulpsimulations', 'Gulp', '', 'gulp'),
    #'mmtksimulations': Engine('mmtksimulations', "Mmtk Newton's Equations", ''),
    #'fireball': Engine('localOrbitalHarmonic', 'Local Orbital DFT Energies, Harmonic Dynamics', ''),
    'vasp': Engine('abinitio','Plane Wave DFT Energies, Harmonic Dynamics','', 'vasp')}


def engines():
    ret = dict(basic_engines)
    from vnf import extensions
    for ext in extensions:
        p = _import('vnf.components.%s' % ext)
        try:
            moreEngines = p.materialSimulationEngines()
        except AttributeError:
            continue
        ret.update(moreEngines)
    return ret


def _import(p):
    return __import__(p, {}, {}, [''])


# version
__id__ = "$Id$"

# End of file 
