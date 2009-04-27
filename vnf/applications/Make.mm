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
PACKAGE = applications


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
	ApproveUser.py \
	Delete.py \
	ITaskApp.py \
	LaunchDetached.py \
	MigrateTable.py \
	PackJobDir.py \
	ProjectTemplator.py \
	RetrieveResults.py \
	SignJar.py \
	Templator.py \
	Timer.py \
	UpdateJobStatus.py \
	WebApplication.py \
	__init__.py \
	configurationSaver.py \
	utils.py \


export:: export-package-python-modules

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $

# End of file
