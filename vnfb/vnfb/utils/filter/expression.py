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


class measure:

    def __init__(self, name):
        self.name = name
        return


    def __eq__(self, s):
        factory = Equal
        if isinstance(s, basestring):
            if s.find('*') != -1:
                factory = Like
            
        return factory(self.name, s)



class CompareOperator(object):

    def __init__(self, measure, value):
        self.measure = measure
        self.value = value
        return


    def __l_and__(self, rhs):
        return And(self, rhs)
        

    def __l_or__(self, rhs):
        return Or(self, rhs)
        


class Equal(CompareOperator):

    def identify(self, visitor):
        return visitor.onEqual(self)


class Like(CompareOperator):

    def identify(self, visitor):
        return visitor.onLike(self)



class LogicalOperator(object):

    pass


class BinaryLogicalOperator(LogicalOperator):

    def __init__(self, left, right):
        self.left = left
        self.right = right
        return


class And(BinaryLogicalOperator):

    def identify(self, visitor):
        return visitor.onAnd(self)


class Or(BinaryLogicalOperator):

    def identify(self, visitor):
        return visitor.onOr(self)
    
    

# version
__id__ = "$Id$"

# End of file 
