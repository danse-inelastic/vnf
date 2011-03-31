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
PACKAGE = qeutils


# directory structure

BUILD_DIRS = \
        filters \
        generators \
        qecalcutils \
        qeparser \
        results \

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
	__init__.py \
        converger.py \
        taskaction.py \
        taskcell.py \
        taskcreator.py \
        taskinfo.py \
        qetasks.py \
        qeconst.py \
        qegrid.py \
        inputinfo.py \
        qeparams.py \
        qerecords.py \
        qescheduler.py \
        qeserver.py \
        nc2dos.py \
        message.py \
        qe2nc.py \
        qeutils.py \
        servers.py \
        jobstatus.py \

#include doxygen/default.def

export:: export-package-python-modules 


#docs: export-doxygen-docs

# version
# $Id: Make.mm 1213 2006-11-18 16:17:08Z linjiao $

# End of file
