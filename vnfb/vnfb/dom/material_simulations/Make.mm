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
PACKAGE = dom/material_simulations


# directory structure

BUILD_DIRS = \

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
	BvKBond.py \
	BvKComputation.py \
	BvKModel.py \
	ComputationResult.py \
	ComputationResultTs.py \
	Eisf.py \
	GulpMd.py \
	GulpOpt.py \
	GulpPhonon.py \
	GulpPotential.py \
	GulpSettings.py \
	Msd.py \
	PhononDOS.py \
	Phonons.py \
	SimulationBase.py \
	Sq.py \
	SQE.py \
	Trajectory.py \
	Vacf.py \
	__init__.py \
	_.py \
	computation_types.py \
	phonon_calculators.py \
	sqe_calculators.py \
	sqe_types.py \


#include doxygen/default.def

export:: export-package-python-modules 


docs: export-doxygen-docs

# version
# $Id: Make.mm 1213 2006-11-18 16:17:08Z linjiao $

# End of file
