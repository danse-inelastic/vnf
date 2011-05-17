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
base class for all visual factories
"""



class AbstractFactory(object):

    
    def __init__(self, director=None, name=None, actor=None):
        """
        director:
        actor: the name of the main actor for the visual
        name: the name to uniquely identify the view to build. it is used
          to create unique ids of UI elements
        """
        self.director = director
        if name is None:
            raise ValueError, "must provide a name"
        self.name = name.replace('/', '-')
        self.actor = actor
        return
    
    
    def build(self, **kwds):
        raise NotImplementedError


# version
__id__ = "$Id$"

# End of file 
