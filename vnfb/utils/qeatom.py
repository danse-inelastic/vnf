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

"Note: not used in VNF"

import json

class QEAtom:
    "Holds essential information about an atom specific to QE."
    def __init__(self, label = "", mass = 0, pseudo = ""):
        self.label   = label
        self.mass    = mass
        self.pseudo  = pseudo

    def props(self):
        "Returns properties of the atom as a list"
        return (self.label, self.mass, self.pseudo)


class QEStructure:
    "(Not used) Holds essential information about the atomic structure composed of one or many QEAtom."
    def __init__(self):
        self.structure   = []

    def append(self, atom):
        self.structure.append(atom.props())

    def dump(self):
        "Serializes structure in json to string"
        return json.dumps(self.structure)

    def load(self, str):
        "Populates structure from string"
        self.structure  = json.loads(str)


def testAtoms():
    import json
    ni  = QEAtom("Ni", 58.6934, "Ni.pbe-nd-rrkjus.UPF")
    cu  = QEAtom("Cu", 63.546, "Cu.pbe-nd-rrkjus.UPF")

    structure   = QEStructure()
    structure.append(ni)
    structure.append(cu)
    dump    = structure.dump()
    print dump

    load    = structure.load(dump)
    print load  # None, why?


def testSimple():
    str = []
    str.append(("a", 1))
    str.append(("b", 2))
    dump    = json.dumps(str)
    print dump

    load    = json.loads(dump)
    print load


if __name__ == "__main__":
    #testAtomList()
    testSimple()

__date__ = "$Jan 16, 2010 10:30:48 PM$"


