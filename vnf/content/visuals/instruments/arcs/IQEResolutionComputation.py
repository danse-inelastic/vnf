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


from IQEResolutionStartPanel import Factory as StartPanel
from IQEResolutionResultsView import Factory as ResultsView
from IQEResolutionTableView import Factory as TableView

from FactoryRoot import FactoryRoot as base
class IQEResolutionComputation(base):

    sub_factory_constructors = {
        'start_panel': StartPanel,
        'results_view': ResultsView,
        'table_view': TableView,
        }


# version
__id__ = "$Id$"

# End of file 
