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
	ins \
	sans \
	tutorials \


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
	AccessControl.py \
	Actor.py \
	Announcer.py \
	Clerk.py \
	Computation.py \
	ComputationResultsRetriever.py \
	CSAccessor.py \
	DBObjectForm.py \
	DistributedDataStorage.py \
	Form.py \
	FormActor.py \
	Geometer.py \
	Instrument.py \
	InstrumentShapeRenderer.py \
	JnlpFile.py \
	Job.py \
	JobBuilder.py \
	Logout.py \
	MaterialSimulation.py \
	NeutronExperiment.py \
	NeutronExperimentWizard.py \
	Postman.py \
	Sample.py \
	Sample2.py \
	SampleAssembly.py \
	SamplePreparation.py \
	SampleInput.py \
	Scatterer.py \
	ScatteringKernel.py \
	Scheduler.py \
	Scribe.py \
	Server.py \
	Shape.py \
	SSHer.py \
	SupportingCalcs.py \
	TreeViewCreator.py \
	UsersFromDB.py \
	inventorylist.py \
	misc.py \
	spawn.py \
	wording.py \
	_extend_class.py \
	__init__.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
