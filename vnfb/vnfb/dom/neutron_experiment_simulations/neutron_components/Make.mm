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

PROJECT = vnfb
PACKAGE = dom/neutron_experiment_simulations/neutron_components


BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	AbstractNeutronComponent.py \
	Monitor.py \
	MonochromaticSource.py \
	SNSModerator.py \
	SNSModeratorMCSimulatedData.py \
	ChanneledGuide.py \
	T0Chopper.py \
	FermiChopper.py \
	SampleComponent.py \
	SampleComponentExample.py \
	EMonitor.py \
	QEMonitor.py \
	QMonitor.py \
	SphericalPSD.py \
	TofMonitor.py \
	DetectorSystem_fromXML.py \
	NeutronRecorder.py \
	VanadiumPlate.py \
	__init__.py \
	_.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
