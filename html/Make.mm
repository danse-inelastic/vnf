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

PROJECT = vnf
PACKAGE = html

RECURSE_DIRS = \
	javascripts \
	css \

EXPORT_DATADIRS = \
	images \
	java \

EXPORT_SYMLINKS = \
	cgi-bin \
	tmp \

INIT_DATAFILES = \
	index.html

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



RSYNC_A = rsync -a --copy-unsafe-links
EXPORT_DATA_PATH = $(EXPORT_ROOT)/$(PROJECT)/$(PACKAGE)


export-package-data: export-package-data-dirs export-package-symlinks init-data-files

export-package-data-dirs:: $(EXPORT_DATADIRS) 
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(EXPORT_DATADIRS); do { \
            if [ -d $$x ]; then { \
	        $(RSYNC_A) $$x/ $(EXPORT_DATA_PATH)/$$x/ ; \
            } fi; \
        } done

CP_SYMLINK = rsync -a
export-package-symlinks:: $(EXPORT_SYMLINKS) 
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(EXPORT_SYMLINKS); do { \
	        $(CP_SYMLINK) $$x $(EXPORT_DATA_PATH)/ ; \
        } done


# copy the data files over only if they do not exist
init-data-files:: $(INIT_DATAFILES)
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(INIT_DATAFILES); do { \
            if [ -e $$x -a ! -e $(EXPORT_DATA_PATH)/$$x ]; then { \
	        $(CP_F) $$x $(EXPORT_DATA_PATH)/ ; \
            } fi; \
        } done


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $

# End of file
