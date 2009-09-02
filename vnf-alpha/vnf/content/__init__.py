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


def announcement():
    from Announcement import Announcement
    return Announcement()


def autorefresh(**kwds):
    from AutoRefresh import AutoRefresh
    return AutoRefresh(**kwds)


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


def image(*args,**kwds):
    from Image import Image
    return Image(*args,**kwds)

def slidableGallery(*args, **kwds):
    from SlidableGallery import SlidableGallery
    return SlidableGallery( *args, **kwds )

def plot_2d(*args, **kwds):
    from Plot_2D import Plot_2D
    return Plot_2D(*args, **kwds)

def imagePlot(*args, **kwds):
    from ImagePlot import ImagePlot
    return ImagePlot(*args, **kwds)

def solidView3D(*args, **kwds):
    from SolidView3D import SolidView3D
    return SolidView3D(*args, **kwds)

def uploader(*args, **kwds):
    from Uploader import Uploader
    return Uploader(*args, **kwds)

def dialog(*args, **kwds):
    from Dialog import Dialog
    return Dialog(*args, **kwds)

def button(*args, **kwds):
    from Button import Button
    return Button(*args, **kwds)

def itaskMonitor(*args, **kwds):
    from ITaskProgress import ITaskProgress
    return ITaskProgress(*args, **kwds)

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




def jssnippet(*args, **kwds):
    from JSsnippet import JSsnippet
    return JSsnippet(*args, **kwds)


# version
__id__ = "$Id: __init__.py,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $"

# End of file 
