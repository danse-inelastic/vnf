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


from Monitor import Monitor as base
class QMonitor(base):

    Qmin = 0.; Qmax = 13.; nQ = 130
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    Qmin = InvBase.d.float( name = 'Qmin', default = 0. )
    Qmax = InvBase.d.float( name = 'Qmax', default = 13.  )
    nQ = InvBase.d.int( name = 'nQ', default = 130 )

    dbtablename = 'qmonitors'
    

QMonitor.Inventory = Inventory
del Inventory


from _ import o2t, AbstractOwnedObjectBase
QMonitorTable = o2t(QMonitor, {'subclassFrom': AbstractOwnedObjectBase})


# version
__id__ = "$Id$"

# End of file 
