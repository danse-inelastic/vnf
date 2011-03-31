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
PACKAGE = dom/neutron_experiment_simulations


# directory structure

BUILD_DIRS = \
	instruments \
	integrated \
	neutron_components \

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
	AbstractNeutronComponent.py \
	GeometricalRelation.py \
	Instrument.py \
	InstrumentConfiguration.py \
	NeutronExperiment.py \
	NeutronStorage.py \
	SampleAssembly.py \
	SampleEnvironment.py \
	Scatterer.py \
	_.py \
	__init__.py \
	computation_types.py \
	instrument_configuration_types.py \
	neutroncomponent_types.py \
	samplecomponent_types.py \
	sample_types.py \


#include doxygen/default.def

export:: export-package-python-modules 


docs: export-doxygen-docs

# version
# $Id: Make.mm 1213 2006-11-18 16:17:08Z linjiao $

# End of file
