#!/usr/bin/env python
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


import unittest
class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwds):
        super(TestCase, self).__init__(*args, **kwds)
        
        from vnf.dom.material_simulations.Phonons import Phonons
        from mccomponents.sample.idf import readDispersion
        datadir = '../../../../content/data/phonons/bvk-bccFeAt295-N40-df0.2'
        nAtoms, dimension, Qaxes, polarizations, energies, dos = readDispersion(datadir)
        disp = Phonons(
            nAtoms = nAtoms,
            dimension = dimension,
            Qaxes = Qaxes,
            polarizations = polarizations,
            energies = energies,
            )
        self.disp = disp
        return
        

    def test3(self):
        disp = self.disp
        b = 1.74
        x,ys = disp.getDispersionPlot(
            [ (b/2,b/2,0),
              (0,0,0),
              (b,0,0),
              (b/2,b/2,b/2),
              (0,0,0),
              ],
            branches=range(3),
            #npointspersegment=31,
            )
        import pylab
        for y in ys:
            pylab.plot(x,y)
        pylab.show()
        raw_input('press ENTER to continue')
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
