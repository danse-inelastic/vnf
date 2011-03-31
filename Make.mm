# -*- Makefile -*-

PROJECT = vnfb

# directory structure

RECURSE_DIRS = \
	bin \
	cgi-bin \
	vnfb \
	dds \
	log \
	content \
	html \
	config \
	tests \
	docs \


#--------------------------------------------------------------------------
#

all: 
	BLD_ACTION="all" $(MM) recurse

