# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = vnfb
PACKAGE = content

RECURSE_DIRS = \

EXPORT_DATADIRS = \
	components \
	documents \


EXPORT_DATAFILES = \

INIT_DATADIRS = \
	data\


OTHERS = \

#--------------------------------------------------------------------------
#

all: export-package-data
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse



RSYNC_A = rsync -a
EXPORT_DATA_PATH = $(EXPORT_ROOT)/$(PROJECT)/$(PACKAGE)

export-package-data:: export-package-datadirs export-package-datafiles


export-package-datadirs:: $(EXPORT_DATADIRS) init-data-dirs
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(EXPORT_DATADIRS); do { \
            if [ -d $$x ]; then { \
	        $(RSYNC_A) $$x $(EXPORT_DATA_PATH)/ ; \
            } fi; \
        } done


export-package-datafiles:: $(EXPORT_DATAFILES) 
	for x in $(EXPORT_DATAFILES); do { \
            if [ -f $$x ]; then { \
	        $(RSYNC_A) $$x $(EXPORT_DATA_PATH)/$$x ; \
            } fi; \
        } done


#initialize some data directories when necessary
#if EXPORT_DATA_PATH/<subdir> already exists, skip; other wise, copy <subdir> over.
init-data-dirs:
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(INIT_DATADIRS); do { \
            if [ -d $$x -a ! -d $(EXPORT_DATA_PATH)/$$x ]; then { \
	        $(RSYNC_A) $$x $(EXPORT_DATA_PATH)/ ; \
            } fi; \
        } done


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $

# End of file
