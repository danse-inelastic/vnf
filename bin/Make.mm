# -*- Makefile -*-

PROJECT = vnf
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
	activateserver.py \
	announce.py \
	approveUser.py \
	checkcod.py \
	checkservers.py \
	checkcod.py \
	createdataobject.py \
	createtable.py \
	cron-daemons.sh \
	cron-monitors.sh \
	deleterecord.py \
	destroydb.py \
	destroydataobject.py \
	doma.py \
	dumpdb.py \
	epscjobdriver.py \
	establishglobalpointers.py \
	establish_ssh_tunnels.py \
	findchildrenofdataobject.py \
	findreferrals.py \
	getuserlist.py \
	initdb.py \
	itaskapp.py \
	launch-detached.py \
	listservers.py \
	loaddataobject.py \
        packjobdir.py \
        jobdriver.py \
	restoredb.py \
	retrieveresults.py \
	run-daemons.sh \
	run-monitors.sh \
	startservices.sh \
	stopservices.sh \
	timer.py \
	updatejobstatus.py \



CP_F = rsync -r --copy-unsafe-links
EXPORT_DATA_PATH = $(EXPORT_ROOT)/$(PROJECT)/$(PACKAGE)

export-data-files::
	mkdir -p $(EXPORT_DATA_PATH); \
	for x in $(EXPORT_DATAFILES); do { \
	  $(CP_F) $$x $(EXPORT_DATA_PATH)/ ; \
	} done

