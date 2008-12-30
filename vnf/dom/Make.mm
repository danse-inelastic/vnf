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
PACKAGE = dom



BUILD_DIRS = \
	ins \
	sans \
	tutorials \
	instruments \
	neutron_components \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	AbInitio.py \
	ACL1.py \
	ACL2.py \
	ACL_Privilege.py \
	ACL_InstrumentSimulationPrivilege.py \
	Analysis.py \
	Block.py \
	Computation.py \
	ComputationResult.py \
	Crystal.py \
	Cylinder.py \
	DbObject.py \
	DummyDataObject.py \
	Disordered.py \
	Geometer.py \
	GulpSimulation.py \
	Instrument.py \
	InstrumentConfiguration.py \
	Job.py \
	MaterialModeling.py \
	MaterialSimulation.py \
	MatterBase.py \
	MmtkSimulation.py \
	NeutronComponent.py \
	NeutronExperiment.py \
	OwnedObject.py \
	PolyCrystal.py \
	ReferenceManager.py \
	ReferenceSet.py \
	Role.py \
	Sample.py \
	SampleAssembly.py \
	SampleEnvironment.py \
	Scatterer.py \
	ScattererExample.py \
	ScatteringKernel.py \
	Server.py \
	Shape.py \
	SingleCrystal.py \
	SqeFromMd.py \
	Table.py \
	User.py \
	idgenerator.py \
	registry.py \
	_all_tables.py \
	_geometer.py \
	_hidden_tables.py \
	_referenceset.py \
	__init__.py \
	acl.py \
	check.py \



export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
