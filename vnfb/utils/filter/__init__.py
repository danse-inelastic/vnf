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


def measure(name, **kwds):
    "create a measure to be used in a filter expression"
    from expression import measure
    return measure(name, **kwds)


def parse(expr, context):
    "parse an expression to create a filter AST"
    from parser import parse
    return parse(expr, context)


def expr2dbsyntax(expr, context):
    ast = parse(expr, context)
    from AST2DBSyntax import AST2DBSyntax
    return AST2DBSyntax().render(ast)


# version
__id__ = "$Id$"

# End of file 
