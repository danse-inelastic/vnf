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


BUILD_DIRS = \
	computation_result_retrievers \
	job_builders \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	__init__.py \
	Actor.py \
	ARCSConfigurationApplyer.py \
	BvK.py \
	Clerk.py \
	Computation.py \
	CSAccessor.py \
	DBObjectForm.py \
	DistributedDataStorage.py \
	Form.py \
	FormActor.py \
	Geometer.py \
	Greeter.py \
	Instrument.py \
	InstrumentConfigurationApplyer.py \
	InstrumentSimulationAppBuilder.py \
	Job.py \
	JobBuilder.py \
	JobDataManager.py \
	MaterialSimulationWizard.py \
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
	BLD_ACTION="export" $(MM) recurse


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
