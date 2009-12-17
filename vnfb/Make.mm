# -*- Makefile -*-
 
PROJECT = vnfb

# directory structure

RECURSE_DIRS = \
	bin \
	cgi-bin \
	vnfb \
	log \
	content \
	html \
	config



#--------------------------------------------------------------------------
#

all: 
	BLD_ACTION="all" $(MM) recurse

