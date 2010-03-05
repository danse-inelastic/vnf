# -*- Python -*-
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


dbname = 'postgres:///vnfbeta'

import os
exportroot = os.environ['EXPORT_ROOT']


vnfbexportroot = os.path.join(exportroot, 'vnfb')
contentroot = os.path.join(vnfbexportroot, 'content')
componentsroot = os.path.join(contentroot, 'components')
dataroot = os.path.join(contentroot, 'data')
configdir = os.path.join(vnfbexportroot, 'config')


lubanserviceshome = '/tmp/luban-services'

pyre_depositories = [
    configdir,
    componentsroot,
    lubanserviceshome,
    ]


# version
__id__ = "$Id$"

# End of file 
