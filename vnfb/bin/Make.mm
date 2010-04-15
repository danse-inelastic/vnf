# -*- Makefile -*-

PROJECT = vnfb
PACKAGE = bin

#--------------------------------------------------------------------------
#

all: export-data-files
	BLD_ACTION="all" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_DATAFILES = \
	announce.py \
	createdefaultformulaformatters.py \
	createdataobject.py \
	createtable.py \
	destroydb.py \
	destroydataobject.py \
	establishglobalpointers.py \
	establish-ssh-tunnels.py \
	establish-ssh-tunnels.sh \
	findreferrals.py \
	getuserlist.py \
	initdb-alpha.py \
	initdb.py \
	initdb.sh \
	itaskapp.py \
	launch-detached.py \
	loaddataobject.py \
        packjobdir.py \
        qedriver.py \
	restorevnfdb.py \
	retrieveresults.py \
	startservices.sh \
	timer.py \
	updatejobstatus.py \
	updatejobstatus.sh \



CP_F = rsync -r --copy-unsafe-links
EXPORT_DATA_PATH = $(EXPORT_ROOT)/$(PROJECT)/$(PACKAGE)

export-data-files::
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(EXPORT_DATAFILES); do { \
	  $(CP_F) $$x $(EXPORT_DATA_PATH)/ ; \
	} done

