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
        from vnfb.components.Postman import Postman
        postman = Postman()
        postman.host = 'localhost'
        postman.port = '50587'
        postman.username = 'linjiao'
        postman.password = 'qiu10-19shi'
        class Msg:
            def as_string(self): return 'test'
        postman.send('linjiao@caltech.edu', 'linjiao@caltech.edu', Msg())
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
