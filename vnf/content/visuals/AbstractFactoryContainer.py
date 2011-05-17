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
container of visual factories
"""



class AbstractFactoryContainer(object):

    
    sub_factory_constructors = {} # sub factories map: name -> constructor of factory
    
    
    def __init__(self, director=None, name=None, actor=None):
        for name1, ctor in self.__class__.sub_factory_constructors.iteritems():
            factory = ctor(director=director, name="%s-%s"%(name,name1), actor=actor)
            setattr(self, name1, factory)
            continue
        return


# version
__id__ = "$Id$"

# End of file 
