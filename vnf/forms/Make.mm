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
PACKAGE = forms


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	DBObjectForm.py \
	Block.py \
	ConfigureNeutronScatterer.py \
	Cylinder.py \
	__init__.py \


export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
