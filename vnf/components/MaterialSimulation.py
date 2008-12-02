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

    def __init__(self, id, short_description, long_description):
        self.id = id
        self.short_description = short_description
        self.long_description = long_description
        return
    

basic_engines = [
    Engine('gulp', 'Gulp', ''),
    Engine('mmtk', "Mmtk Newton's Equations", ''),
    Engine('localOrbitalHarmonic', 'Local Orbital DFT Energies, Harmonic Dynamics', ''),
    Engine('planeWaveHarmonic','Plane Wave DFT Energies, Harmonic Dynamics',''),
    ]


def engines():
    ret = list(basic_engines)
    from vnf import extensions
    for ext in extensions:
        p = _import('vnf.components.%s' % ext)
        try:
            more = p.materialSimulationEngines()
        except AttributeError:
            continue
        ret += more
    return ret


def _import(p):
    return __import__(p, {}, {}, [''])


# version
__id__ = "$Id$"

# End of file 
