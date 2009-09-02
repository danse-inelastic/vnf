# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = vnf
PACKAGE = content



BUILD_DIRS = \
	table \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	Action.py \
	ActionRequireAuthentication.py \
	Announcement.py \
	AutoRefresh.py \
	Button.py \
	Dialog.py \
	Image.py \
	ImagePlot.py \
	ITaskProgress.py \
	JSsnippet.py \
	Page.py \
	Plot_2D.py \
	SlidableGallery.py \
	SolidView3D.py \
	TreeView.py \
	Uploader.py \
	__init__.py


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
