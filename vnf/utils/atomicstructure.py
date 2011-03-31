# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def makeXYZfileContent(structure, **kwds):
    '''create a list of strings (each string is one line) as the content
    of the xyz file for the given structure
    '''
    # get "parser"
    from matter.Parsers import getParser
    xyz = getParser('xyz')
    
    # content strings
    content = xyz.toLines(structure, **kwds)
    
    return content


# version
__id__ = "$Id$"

# End of file 
