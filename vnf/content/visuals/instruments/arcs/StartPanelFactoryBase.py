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


import luban.content

class Factory(object):

    def __init__(self, director):
        self.director = director
        return
    

    def build(self):
        raise NotImplementedError


    def buildViewIndicator(self):
        # where am I?
        path = [
            ('<< ARCS portal', 
             luban.content.load(
                    actor='instruments/arcs', 
                    routine='reloadStartPanel'
                    )
             ),
            ]
        from ... import view_indicator
        whereami = view_indicator.visual(path)
        return whereami


# version
__id__ = "$Id$"

# End of file 
