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


# describe geometrical relation of two entities: "target" relative to "reference"

class GeometricalRelation:

    targetname = ''
    position = [0.,0.,0.]
    orientation = [[1.,0.,0.],
                   [0.,1.,0.],
                   [0.,0.,1.],]
    referencename = ''


from _ import o2t
GeometricalRelationTable = o2t(GeometricalRelation)



# version
__id__ = "$Id$"

# End of file 
