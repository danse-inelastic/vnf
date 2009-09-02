#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from opal.applications.WebApplication import WebApplication as Base


class WebApplication(Base):


    def main(self, *args, **kwds):
        Base.main(self, *args, **kwds)
        return


    def _getPrivateDepositoryLocations(self):
        return ['content', 'config']
        #return ['../content', '../config']


# version
__id__ = "$Id: WebApplication.py,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $"

# End of file 
