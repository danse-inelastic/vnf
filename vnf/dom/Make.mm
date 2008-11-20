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
	neutron_components \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	Block.py \
	Computation.py \
	ComputationResult.py \
	Crystal.py \
	Cylinder.py \
	DbObject.py \
	DummyDataObject.py \
	DetectorSystem_fromXML.py \
	Disordered.py \
	Geometer.py \
	Instrument.py \
	InstrumentConfiguration.py \
	IQEMonitor.py \
	IQMonitor.py \
	Job.py \
	MaterialModeling.py \
	MaterialSimulation.py \
	MatterBase.py \
	MonochromaticSource.py \
	NeutronComponent.py \
	NeutronExperiment.py \
	OwnedObject.py \
	PolyCrystal.py \
	ReferenceSet.py \
	Sample.py \
	SampleAssembly.py \
	SampleComponent.py \
	SampleEnvironment.py \
	Scatterer.py \
	ScattererExample.py \
	ScatteringKernel.py \
	Server.py \
	Shape.py \
	SingleCrystal.py \
	Table.py \
	User.py \
	idgenerator.py \
	registry.py \
	_all_tables.py \
	_geometer.py \
	_hidden_tables.py \
	_referenceset.py \
	__init__.py \



export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
