# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from filter import Filter

TYPE    = "pw"

"""
PWFilter - configuration input filter for pw task type. 
            It combines positive and negative input filters
"""

class PWFilter(Filter):

#    def __init__(self):
#        Filter.__init__(self, TYPE)


    def _setPlusFilter(self):
        


    def _setMinusFilter(self):
        

        

# Remove: pseudo_dir
# Remove: outdir
# Set prefix = 'pwscf'



__date__ = "$Aug 6, 2010 12:16:13 PM$"


