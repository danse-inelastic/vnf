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

# Test of the pseudo potential list

from orderedDict import OrderedDict

PSEUDO = OrderedDict()
PSEUDO["Ag"] = (
                "Ag.pbe-d-rrkjus.info",
                "Ag.pbe-d-rrkjus.UPF",
                "Ag.pz-d-rrkjus.UPF"
                )

PSEUDO["Al"] = (
                "Al.blyp-n-van_ak.info",
                "Al.blyp-n-van_ak.UPF",
                "Al.bp-n-van_ak.info",
                "Al.bp-n-van_ak.UPF"
                )

# As, Au, etc...

def testPseudo():
    # Print
    print PSEUDO[PSEUDO.keys()[0]][0]


if __name__ == "__main__":
    testPseudo()

__date__ = "$Jan 19, 2010 6:39:30 AM$"


