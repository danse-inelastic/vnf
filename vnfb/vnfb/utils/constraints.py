# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Variable(object):

    def __eq__(self, right):
        return Equal(self, right)


class Relation(object): pass


class BinaryRelation(Relation):

    def __init__(self, left, right):
        self.left = left
        self.right = right
        

class Equal(BinaryRelation):

    pass
    

# version
__id__ = "$Id$"

# End of file 
