#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

class THGenerator(object):
    "Generator for CP Dynamics with Thermostat task"

    def __init__(self, director, inventory, input = None):
        self._director  = director
        self._inv       = inventory
        self._input     = input

__date__ = "$May 16, 2010 10:04:32 AM$"


