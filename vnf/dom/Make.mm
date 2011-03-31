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

PROJECT = vnf
PACKAGE = dom


# directory structure

BUILD_DIRS = \
	analysis \
	geometry \
	material_simulations \
	neutron_experiment_simulations \
	scattering_kernels \

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
	AbstractOwnedObjectTsBase.py \
	Atom.py \
	AtomicStructure.py \
	Bug.py \
	Computable.py \
	Computation.py \
	ComputationResult.py \
	ComputationResultTs.py \
	Export.py \
	Feature.py \
	Histogram.py \
	ITask.py \
	Job.py \
	Label.py \
	Lattice.py \
	MaterialSimulation.py \
	News.py \
	OwnedObject.py \
	OwnedObjectTs.py \
	Privilege.py \
	QEConfiguration.py \
	QEConvergence.py \
	QEConvParamTask.py \
	QEJob.py \
	QEConvParam.py \
	QESetting.py \
	QESimulation.py \
	QESimulationTask.py \
	QETask.py \
	Registrant.py \
	Role.py \
	RoleHasPrivilege.py \
	RoleHasRole.py \
	Server.py \
	SmartLabel.py \
	UnitCell.py \
	User.py \
	UserHasRole.py \
	UserSetting.py \
	__init__.py \
	_.py \
	computation_types.py \


#include doxygen/default.def

export:: export-package-python-modules 


docs: export-doxygen-docs

# version
# $Id: Make.mm 1213 2006-11-18 16:17:08Z linjiao $

# End of file
