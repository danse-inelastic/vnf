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


# base class for visual factory root
# it contains various factories for building visuals
# those factories may still have sub-factories


from ...AbstractFactoryContainer import AbstractFactoryContainer
class FactoryRoot(AbstractFactoryContainer):

    sub_factory_constructors = {
        'start_panel': None,
        'results_view': None,
        }


# version
__id__ = "$Id$"

# End of file 
