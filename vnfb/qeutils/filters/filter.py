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

from vnf.qeutils.qeparser.filter import Filter as InputFilter

"""
Filter - base class for all filters. Performs no filtering
         It combines positive and negative input filters
"""

class Filter(object):

    def __init__(self):
        self._plus      = InputFilter("fplus")
        self._minus     = InputFilter("fminus")
        self._setPlusFilter()
        self._setMinusFilter()


    def _setPlusFilter(self):
        pass    # No implementation


    def _setMinusFilter(self):
        pass    # No implementation


    def apply(self, input):
        """
        Apply filter to input object

            input: (object: QEInput) 
        """
        self._plus.apply(input, "plus")
        self._minus.apply(input, "minus")


__date__ = "$Aug 6, 2010 12:31:10 PM$"


