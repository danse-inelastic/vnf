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
	Arm.py \
	ChanneledGuide.py \
	CollimatorLinear.py \
	CollimatorRadial.py \
	DetectorSystem_fromXML.py \
	DiskChopper.py \
	EMonitor.py \
	FermiChopper.py \
	Guide.py \
	GuideGravity.py \
	LMonitor.py \
	Monitor.py \
	MonitorBase.py \
	MonochromaticSource.py \
	NDMonitor.py \
	NeutronPlayer.py \
	NeutronRecorder.py \
	PSDMonitor.py \
	PSD_TEWMonitor.py \
	PlaceHolder.py \
	QEMonitor.py \
	QMonitor.py \
	SampleBase.py \
	SampleComponent.py \
	SimpleSource.py \
	Slit.py \
	SNSModerator.py \
	SNSModeratorMCSimulatedData.py \
	SphericalPSD.py \
	TofMonitor.py \
	T0Chopper.py \
	VulcanDetectorSystem.py \
	VanadiumPlate.py \
	__init__.py \
	_.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
