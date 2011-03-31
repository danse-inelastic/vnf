# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from OwnedObject import OwnedObject as base
class SmartLabel(base):
    
    name = 'smartlabels'
    
    import dsaw.db
    
    targettable = dsaw.db.varchar(name='targettable', length=64)
    label = dsaw.db.varchar(name='label', length=64)
    filter_expr = dsaw.db.varchar(name='filter_expr', length=512)
    filter_key = dsaw.db.varchar(name='filter_key', length=64)
    filter_value = dsaw.db.varchar(name='filter_value', length=256)



def getFilterExpr(slabel):
    if slabel.filter_expr: return slabel.filter_expr
    return "%s=='%s'" % (slabel.filter_key, slabel.filter_value)


# version
__id__ = "$Id$"

# End of file 
