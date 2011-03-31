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


'''
This test whether the data objects for the computations
are handled well by dsaw orm mapper.
'''

# standalone = True


import unittest
class TestCase(unittest.TestCase):

    def test(self):
        from vnfb.components.DOMAccessor import DOMAccessor
        domaccessor = DOMAccessor('t')
        
        from vnfb.dom.computation_types import typenames, deps_typenames
        for name in typenames+deps_typenames:
            domaccessor._getObjectByImportingFromDOM(name)
            
        return



def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
