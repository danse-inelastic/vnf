# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


jrnltag = 'computation_result_retrievers'
import journal
warning = journal.warning(jrnltag)


def getHandler(self, component):
    type = component.__class__.__name__
    module = 'neutron_components.%s' % type
    try:
        module = __import__(module, {}, {}, [''])
    except ImportError:
        # means handler not implemented
        if _isMonitor(component): warning.log('handler for %s not implemented' % type)
        return
    return module.retrieve


from vnf.dom.neutron_components.Monitor import Monitor
def _isMonitor(m): return isinstance(m, Monitor)


# version
__id__ = "$Id$"

# End of file 
