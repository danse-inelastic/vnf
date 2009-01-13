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
PACKAGE = components/job_builders


BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	AbInitio.py \
	InstrumentConfigurationApplyer.py \
	InstrumentSimulationAppBuilder.py \
	JobBuilder.py \
	McstasSampleBuilder.py \
	McvineSampleAssemblyBuilder.py \
	McvineScattererXMLBuilder.py \
	NeutronExperiment.py \
	NeutronExperimentSimulationRunBuilder.py \
	PhononsFromAbinitio.py \
	SampleAssemblyXMLBuilder.py \
	__init__.py \
	_utils.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
