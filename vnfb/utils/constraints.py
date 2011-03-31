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


    def __init__(self, name=None):
        self.name = name
        return


    def __str__(self):
        return self.name


    def identify(self, visitor): return visitor.onVariable(self)
    

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


    def identify(self, visitor):
        return visitor.onEqual(self)
    
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

    def identify(self, visitor):
        return visitor.onAddition(self)
    
    pass


class Subtraction(BinaryOperation):
    op = '-'

    def identify(self, visitor):
        return visitor.onSubtraction(self)
    
    pass


class Multiplication(BinaryOperation):
    op = '*'

    def identify(self, visitor):
        return visitor.onMultiplication(self)
    
    pass


class Division(BinaryOperation):
    op = '/'

    def identify(self, visitor):
        return visitor.onDivision(self)
    
    pass




class Evaluator(object):


    def __init__(self, environ):
        self.environ = environ
        return


    def evaluate(self, expression):
        if self.isNumber(expression): return expression
        return expression.identify(self)


    def isNumber(self, c):
        return isinstance(c, int) or isinstance(c, float)


    def onEqual(self, e):
        return self.evaluate(e.left) == self.evaluate(e.right)


    def onAddition(self, e):
        return self.evaluate(e.left)+self.evaluate(e.right)


    def onSubtraction(self, e):
        return self.evaluate(e.left)-self.evaluate(e.right)


    def onMultiplication(self, e):
        return self.evaluate(e.left)*self.evaluate(e.right)


    def onDivision(self, e):
        return self.evaluate(e.left)/self.evaluate(e.right)


    def onVariable(self, v):
        return self.environ[v.name]
        


def check(constraint, environ):
    '''check if a constraint is satisfied in a given environment'''
    return Evaluator(environ).evaluate(constraint)


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        a = Variable('a')
        b = Variable('b')
        expr = a == b
        self.assertEqual(check(expr, {'a': 2, 'b':3}), False)
        self.assertEqual(check(expr, {'a': 2, 'b':2}), True)
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
