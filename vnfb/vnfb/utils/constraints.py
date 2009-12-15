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


# a, b, c, ...
class Variable:

    def __add__(self, right):
        return Addition(self, right)


    def __mul__(self, right):
        return Multiplication(self, right)


    def __eq__(self, right):
        return Equal(self, right)


# a = b, a>3, ...
class Relation(object): pass


class BinaryRelation(Relation):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '%s %s %s' % (self.left, self.relation, self.right)

class Equal(BinaryRelation):

    relation = '=='
    
    pass



# a+b, b*c, ...
class Operation(object):

    def __eq__(self, right):
        return Equal(self, right)


class BinaryOperation(Operation):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right


    def __str__(self):
        return '%s %s %s' % (self.left, self.op, self.right)


class Addition(BinaryOperation):
    op = '+'
    pass


class Subtraction(BinaryOperation):
    op = '-'
    pass


class Multiplication(BinaryOperation):
    op = '*'
    pass


class Division(BinaryOperation):
    op = '/'
    pass


# version
__id__ = "$Id$"

# End of file 
