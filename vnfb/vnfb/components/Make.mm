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

PROJECT = vnfb
PACKAGE = components


# directory structure

BUILD_DIRS = \
	geometry \
	iworkers \
	job_builders \
	scattering_kernels \
	visuals \

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
	AccessControl.py \
	AdminActor.py \
	Announcer.py \
	AppExtension.py \
	AuthorizedActor.py \
	Clerk.py \
	ComputationResultRetriever.py \
	CSAccessor.py \
	DistributedDataStorage.py \
	DOMAccessor.py \
	JnlpFile.py \
        Job.py \
	JobBuilder.py \
	MasterTable.py \
	Postman.py \
        QEAnalysis.py \
        QEConvergence.py \
        QEGenerator.py \
        QESettings.py \
        QETable.py \
        Scheduler.py \
	SSHer.py \
	UsersFromDB.py \
	__init__.py \


#include doxygen/default.def

export:: export-package-python-modules 


docs: export-doxygen-docs

# version
# $Id: Make.mm 1213 2006-11-18 16:17:08Z linjiao $

# End of file
