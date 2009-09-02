# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from DbObject import DbObject
class Crystal(DbObject):

    name = 'crystals'

    import dsaw.db

    chemical_formula = dsaw.db.varchar( name='chemical_formula', length = 1024 )
    chemical_formula.meta['tip'] = "chemical formula"

    datafile = dsaw.db.varchar( name='datafile', length = 1024 )
    datafile.meta['tip'] = 'data file name'

    pass # end of Crystal


# version
__id__ = "$Id$"

# End of file 
