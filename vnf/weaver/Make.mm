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
PACKAGE = weaver



BUILD_DIRS = \
	table \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	AccordionMill.py \
	ActionHrefRenderer.py \
	ActionLinkRenderer.py \
	ActionMill_forForm.py \
	AutoRefreshRenderer.py \
	DocumentMill.py \
	DocumentMillExtensions.py \
	ImagePlotMill.py \
	JavaScriptWeaver.py \
	JavaScriptWeaverBase.py \
	JavaScriptWeaverExtensions.py \
	Jnlp.py \
	JnlpMill.py \
	PageMill.py \
	Plot_2DMill.py \
	SlidableGallery.py \
	SolidView3DMill.py \
	StructuralMill.py \
	TableMill.py \
	TreeViewMill.py \
	UploaderMill.py \
	__init__.py \
	_utils.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
