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
PACKAGE = html/css

RECURSE_DIRS = \

EXPORT_DATADIRS = \
	jquery\
	luban\
	skeleton\
	tabulator\


EXPORT_DATAFILES = \
	luban.css\
	vnf.css \
	vnf-atomicstructure.css \
	vnf-bvk.css \
	vnf-epsc.css \
	vnf-experiment.css \
	vnf-jobs.css \
	vnf-login.css \
	vnf-mainframe.css \
	vnf-mastertable.css \
	vnf-matsim.css \
	vnf-matter-overview.css \
	vnf-objecteditor.css \
        vnf-qe.css \
        vnf-sample.css \
	vnf-table.css \



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



#RSYNC_A = rsync -a --copy-unsafe-links
RSYNC_A = cp -rf
EXPORT_DATA_PATH = $(EXPORT_ROOT)/$(PROJECT)/$(PACKAGE)


export-package-data: export-package-data-dirs export-package-data-files


export-package-data-dirs:: $(EXPORT_DATADIRS) 
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(EXPORT_DATADIRS); do { \
            if [ -d $$x ]; then { \
	        $(RSYNC_A) $$x/ $(EXPORT_DATA_PATH)/$$x/ ; \
            } fi; \
        } done

export-package-data-files:: $(EXPORT_DATAFILES) 
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(EXPORT_DATAFILES); do { \
	        $(RSYNC_A) $$x $(EXPORT_DATA_PATH)/ ; \
        } done


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $

# End of file
