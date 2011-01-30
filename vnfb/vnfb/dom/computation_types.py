# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


typenames = []
deps_typenames = [
    'Histogram.Histogram',
    ]


from material_simulations.computation_types import \
     typenames as ts, deps_typenames as dts
typenames+=ts
deps_typenames+=dts

from analysis.analysis_types import \
     typenames as ts, deps_typenames as dts
typenames+=ts
deps_typenames+=dts

from neutron_experiment_simulations.computation_types import \
     typenames as ts, deps_typenames as dts
typenames+=ts
deps_typenames+=dts



# version
__id__ = "$Id$"

# End of file 
