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
exportroot = os.environ.get('EXPORT_ROOT') or os.environ.get('PYRE_DIR')
if not exportroot:
    raise RuntimeError, "cannot figure out export root directory"


vnfbexportroot = os.path.join(exportroot, 'vnfb')
contentroot = os.path.join(vnfbexportroot, 'content')
componentsroot = os.path.join(contentroot, 'components')
dataroot = os.path.join(contentroot, 'data')
configdir = os.path.join(vnfbexportroot, 'config')
guid_datastore_path = os.path.join(configdir, 'guid.dat')

lubanserviceshome = '/tmp/luban-services'

pyre_depositories = [
    configdir,
    componentsroot,
    lubanserviceshome,
    ]


# version
__id__ = "$Id$"

# End of file 
