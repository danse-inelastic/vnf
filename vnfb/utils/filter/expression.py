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

    def __init__(self, name, type=None):
        if type is None:
            type = 'str'
            
        self.name = name
        self.type = type
        return


    def __eq__(self, s):
        factory = Equal
        
        # in some cases, == actually means "like"
        # need a more robust implementation
        if isinstance(s, basestring):
            if s.find('*') != -1:
                factory = Like
            
        return factory(self, s)


    def __str__(self):
        return "%s(%s)" % (self.name, self.type)


class Operator(object):

    def __l_and__(self, rhs):
        return And(self, rhs)
        

    def __l_or__(self, rhs):
        return Or(self, rhs)
        


class CompareOperator(Operator):

    def __init__(self, measure, value):
        self.measure = measure
        self.value = value
        return



class Equal(CompareOperator):

    def identify(self, visitor):
        return visitor.onEqual(self)


    def __str__(self):
        return '(%s == %s)' % (self.measure, self.value)


class Like(CompareOperator):

    def identify(self, visitor):
        return visitor.onLike(self)


    def __str__(self):
        return '(%s like %s)' % (self.measure, self.value)



class LogicalOperator(Operator):

    pass


class BinaryLogicalOperator(LogicalOperator):

    def __init__(self, left, right):
        self.left = left
        self.right = right
        return


class And(BinaryLogicalOperator):

    def identify(self, visitor):
        return visitor.onAnd(self)


    def __str__(self):
        return '(%s and %s)' % (self.left, self.right)


class Or(BinaryLogicalOperator):

    def identify(self, visitor):
        return visitor.onOr(self)
    
    
    def __str__(self):
        return '(%s or %s)' % (self.left, self.right)



# version
__id__ = "$Id$"

# End of file 
