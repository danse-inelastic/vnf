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
        
        from vnfb.dom.material_simulations.PhononDispersion import PhononDispersion
        from mccomponents.sample.idf import readDispersion
        datadir = '../../../../content/data/phonondispersions/bvk-fccAgAt293-N20-df0.2'
        nAtoms, dimension, Qaxes, polarizations, energies, dos = readDispersion(datadir)
        disp = PhononDispersion(
            nAtoms = nAtoms,
            dimension = dimension,
            Qaxes = Qaxes,
            polarizations = polarizations,
            energies = energies,
            )
        self.disp = disp
        return
        

    def test(self):
        disp = self.disp
        energies = disp.energies
        self.assertAlmostEqual(disp.energy( Q=(0,0,0), branch=0 ), energies[0,0,0,0])
        self.assertAlmostEqual(disp.energy( Q=(0,0,0), branch=1 ), energies[0,0,0,1])
        self.assertAlmostEqual(disp.energy( Q=(0,0,0), branch=2 ), energies[0,0,0,2])
        print disp.energy( Q=(0,0,3.08), branch=0)
        return


    def test2(self):
        disp = self.disp
        x,y = disp.getDispersionCurve((0,0,0), (0,0,3.08), branch=0, npoints=20)
        import pylab
        pylab.plot(x,y)
        pylab.show()
        return

    
    def test3(self):
        disp = self.disp
        x,ys = disp.getDispersionPlot(
            [ (0,0,0),
              (0,0,1.54),
              (0,1.54,1.54),
              (0,0,0),
              (0.77,0.77,0.77),
              ],
##             [(0,0,0),
##              (3.08,3.08,3.08),
##              (1.54, 1.54, 0),
##              (1.54, 1.54, 1.54),
##              (1.54, 2.31, 0.77),
##              ],
             branches=range(3), npointspersegment=31)
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