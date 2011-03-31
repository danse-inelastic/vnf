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

    def test1(self):
        'create a SQE histogram from function and plot it'
        from histogram  import histogram, arange
        sqe = histogram(
            name = 'S(Q,E)',
            axes = [('Q', arange(0,12,0.1), 'angstrom**-1'),
                    ('E', arange(-50,50, 1.), 'meV')],
            fromfunction = lambda q,e: q**2+e**2,
            )
        if interactive:
            from histogram.plotter import defaultPlotter
            defaultPlotter.plot(sqe)
        return
        
    
    def test2(self):
        'create a SQE histogram from data and plot it'
        from histogram  import histogram, arange
        sqe = histogram(
            name = 'S(Q,E)',
            axes = [('Q', arange(0,12,0.1), 'angstrom**-1'),
                    ('E', arange(-50,50, 1.), 'meV')],
            )
        sqe.I[:] = 1
        if interactive:
            from histogram.plotter import defaultPlotter
            defaultPlotter.plot(sqe)
        return
        
    
interactive = False
def main():
    global interactive
    interactive = True
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
