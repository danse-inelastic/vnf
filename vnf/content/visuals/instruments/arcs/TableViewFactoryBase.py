# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


"""
base class for visuals that shows a table of computaions
"""



import luban.content


from ...TableFactory import TableViewFactory as base
class Factory(base):
    
    
    def __init__(self, director=None, name=None, actor=None):
        super(Factory, self).__init__(director=director, name=name, actor=actor)
        return



# version
__id__ = "$Id$"

# End of file 
