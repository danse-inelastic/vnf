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

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	AbstractOwnedObjectBase.py \
	AbInitio.py \
	Activity.py \
	ACL1.py \
	ACL2.py \
	ACL_Privilege.py \
	ACL_InstrumentSimulationPrivilege.py \
	Analysis.py \
	Atom.py \
	AtomicStructure.py \
	Block.py \
	Computation.py \
	ComputationResult.py \
	Crystal.py \
	CrystallineMatterBase.py \
	Cylinder.py \
	DbObject.py \
	DummyDataObject.py \
	Disordered.py \
	Geometer.py \
	GulpPotential.py \
	GulpResults.py \
	GulpSimulation.py \
	Instrument.py \
	InstrumentConfiguration.py \
	ITask.py \
	Job.py \
	Label.py \
	Lattice.py \
	MaterialModeling.py \
	MaterialSimulation.py \
	MatterBase.py \
	MdAnalysis.py \
	MmtkSimulation.py \
	NeutronComponent.py \
	NeutronExperiment.py \
	OwnedObject.py \
	PhononsFromAbinitio.py \
	PolyCrystal.py \
	ReferenceManager.py \
	ReferenceSet.py \
	Registrant.py \
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
	SmartLabel.py \
	Table.py \
	User.py \
	VASP.py \
	idgenerator.py \
	registry.py \
	_all_tables.py \
	_geometer.py \
	_hidden_tables.py \
	_referenceset.py \
	__init__.py \
	acl.py \
	check.py \
	hash.py \



export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
