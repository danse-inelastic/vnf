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


dbname = 'postgres:///vnfeta'

import os
exportroot = os.environ.get('EXPORT_ROOT') or os.environ.get('PYRE_DIR')
if not exportroot:
    raise RuntimeError, "cannot figure out export root directory"


vnfexportroot = os.path.join(exportroot, 'vnf')
contentroot = os.path.join(vnfexportroot, 'content')
componentsroot = os.path.join(contentroot, 'components')
dataroot = os.path.join(contentroot, 'data')
configdir = os.path.join(vnfexportroot, 'config')
guid_datastore_path = os.path.join(configdir, 'guid.dat')

lubanserviceshome = '/tmp/luban-services'

pyre_depositories = [
    configdir,
    componentsroot,
    lubanserviceshome,
    ]


controller_url = ""
html_base = ""

# version
__id__ = "$Id$"

# End of file 
