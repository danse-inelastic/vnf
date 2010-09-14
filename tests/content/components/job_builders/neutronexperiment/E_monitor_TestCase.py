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


from testneutroncomponent import createTestCase

from vnfb.dom.neutron_experiment_simulations.neutron_components.EMonitor import EMonitor


TestCase = createTestCase(EMonitor)
    

def main():
    import unittest
    unittest.main()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
