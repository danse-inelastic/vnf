# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def scheduler( name ):
    package = 'vnfb.clusterscheduler'
    module = __import__( '%s.%s' % (package,name), {}, {}, [''] )
    #exec 'import %s as module' % name in locals()
    return module.Scheduler


# version
__id__ = "$Id$"

# End of file 
