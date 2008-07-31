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

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	__init__.py \
	AbInitio.py \
	ARCSconfiguration.py \
	Block.py \
	Component.py \
	ConfiguredInstrument.py \
	ConfiguredScatterer.py \
	Crystal.py \
	Cylinder.py \
	DbObject.py \
	DetectorSystem_fromXML.py \
	Disordered.py \
	GulpScatteringKernel.py \
	IDFPhononDispersion.py \
	Instrument.py \
	IQEMonitor.py \
	Job.py \
	Matter.py \
	MatterBase.py \
	MonochromaticSource.py \
	NeutronExperiment.py \
	OwnedObject.py \
	PhononDispersion.py \
	PolyCrystal.py \
	PolyXtalCoherentPhononScatteringKernel.py \
	PositionOrientationRegistry.py \
	ReferenceSet.py \
	Sample.py \
	SampleAssembly.py \
	SampleEnvironment.py \
	Scatterer.py \
	ScatteringKernel.py \
	Server.py \
	Shape.py \
	ShapeBase.py \
	SimulationResult.py \
	SingleCrystal.py \
	Table.py \
	User.py \
	VirtualObject.py \



export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
