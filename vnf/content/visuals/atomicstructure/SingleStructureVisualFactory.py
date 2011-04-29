# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# base class of view factories for one structure


import luban.content as lc


class Factory(object):

    def __init__(self, director, id):
        self.director = director
        self.id = id
        self.domaccess = director.retrieveDOMAccessor('atomicstructure')
        self.atomicstructure = self.domaccess.getAtomicStructure(id)
        self.record = self.domaccess.orm(self.atomicstructure)
        self.actor = 'atomicstructure'


    def getAtomicStructureLabel(self):
        return self.domaccess.getAtomicStructureLabel(self.id)



# version
__id__ = "$Id$"

# End of file 
