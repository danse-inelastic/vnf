#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def page(**kwds):
    from Page import Page
    return Page(**kwds)

def portletPage(**kwds):
    from PortletPage import PortletPage
    return PortletPage(**kwds)

def action(*args, **kwds):
    from Action import Action
    return Action( *args, **kwds )


def actionRequireAuthentication(*args, **kwds):
    from ActionRequireAuthentication import ActionRequireAuthentication
    return ActionRequireAuthentication( *args, **kwds )


def treeview(*args, **kwds ):
    from TreeView import TreeView
    return TreeView(*args, **kwds )

def branch(*args, **kwds):
    from TreeView import Branch
    return Branch( *args, **kwds )

def leaf(*args, **kwds):
    from TreeView import Leaf
    return Leaf( *args, **kwds )

treeview.branch = branch
treeview.leaf = leaf
del branch, leaf

# version
__id__ = "$Id: __init__.py,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $"

# End of file 
