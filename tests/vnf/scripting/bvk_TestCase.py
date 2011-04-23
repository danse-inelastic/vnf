#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


skip = True

from vnf import scripting
scripting.runByHttp.controller_url = 'http://192.168.12.150/cgi-bin/vnf/dev.cgi'


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        model_id='6P343XN'
        from vnf.scripting import authenticate
        from realuser import username, password
        credential = authenticate(username=username, password=password)
        from vnf.scripting.bvk.phonons import compute
        compute(model_id, credential=credential)
        return

    
    def test2(self):
        computationid = 'LHHD5P3'
        from vnf.scripting import authenticate
        from realuser import username, password
        credential = authenticate(username=username, password=password)
        from vnf.scripting.bvk.phonons import createPlot
        createPlot(computationid, credential)
        return


def main():
    from vnf.deployment import vnfexportroot
    import os
    bindir = os.path.join(vnfexportroot, 'bin')
    os.chdir(bindir)
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id: PyCifRW_TestCase.py 3678 2011-03-31 22:13:43Z linjiao $"

# End of file 

