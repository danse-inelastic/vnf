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
PACKAGE = components


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	__init__.py \
	Actor.py \
	ARCSConfigurationApplyer.py \
	Clerk.py \
	CSAccessor.py \
	DBObjectForm.py \
	Form.py \
	FormActor.py \
	Geometer.py \
	Greeter.py \
	Instrument.py \
	InstrumentConfigurationApplyer.py \
	InstrumentSimulationAppBuilder.py \
	Job.py \
	JobDataManager.py \
	McstasSampleBuilder.py \
	McvineSampleAssemblyDatafilesCollector.py \
	McvineSampleAssemblyBuilder.py \
	McvineScattererXMLBuilder.py \
	NeutronExperiment.py \
	NeutronExperimentWizard.py \
	NeutronExperimentSimulationRunBuilder.py \
	NeutronExperimentSimulationRunBuilder_demo.py \
	PyHtmlTable.py \
	Sample.py \
	SampleAssembly.py \
	SampleAssemblyXMLBuilder.py \
	SampleInput.py \
	SamplePreparation.py \
	Scatterer.py \
	ScattererConfigurationApplyer.py \
	ScatteringKernel.py \
	ScatteringKernelInput.py \
	Scheduler.py \
	Scribe.py \
	Server.py \
	Shape.py \
	SSHer.py \
	SupportingCalcs.py \
	TreeViewCreator.py \
	inventorylist.py \
	misc.py \
	spawn.py \
	twodarr.py \
	wording.py \


export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
