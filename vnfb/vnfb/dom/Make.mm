# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = vnfb
PACKAGE = dom


# directory structure

BUILD_DIRS = \
	material_simulations \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)


#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	AbstractOwnedObjectBase.py \
	Atom.py \
	AtomicStructure.py \
	Computation.py \
	Job.py \
	Lattice.py \
	OwnedObject.py \
	Server.py \
	UnitCell.py \
	__init__.py \
	_.py \
	computation_types.py \


#include doxygen/default.def

export:: export-package-python-modules 


docs: export-doxygen-docs

# version
# $Id: Make.mm 1213 2006-11-18 16:17:08Z linjiao $

# End of file
