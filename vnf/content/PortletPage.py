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


from vnf.content.Page import Page as Base


class PortletPage(Base):


    def __init__(self, name, title, root):
        Base.__init__(self, name, title, root)



        return


# version
__id__ = "$Id: Page.py,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $"

# End of file 
