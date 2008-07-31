#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Node:

    def __init__(self, label, action = None):
        self.label = label
        self.action = action
        return


    def identify(self, visitor):
        raise NotImplementedError



class Leaf(Node):

    def identify(self, visitor):
        return visitor.onLeaf( self )


class Branch(Node):

    def __init__(self, label, action = None, children = None):
        Node.__init__(self, label, action = action)
        if children is None: children = []
        self.children = children
        return


    def addChild(self, child):
        self.children.append( child )
        return


    def identify(self, renderer):
        return renderer.onBranch(self)
        


class TreeView(Branch):

    def identify(self, visitor):
        return visitor.onTreeView(self)


# version
__id__ = "$Id$"

# End of file 
