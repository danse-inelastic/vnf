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


from SingleStructureVisualFactory import Factory as base
class Factory(base):

    def createViewIndicator(self):
        path = []

        actor = self.actor
        path.append(('Atomic Structures', lc.load(actor=actor)))

        label = self.getAtomicStructureLabel()
        action = lc.load(actor=actor, routine='showOverview', id = self.id,)
        path.append((label,action))

        path.append('details')
        
        return self.director.retrieveVisual('view-indicator', path=path)




# version
__id__ = "$Id$"

# End of file 
