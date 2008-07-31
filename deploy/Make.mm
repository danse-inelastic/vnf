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

#proposed?

#temporarily reset all environment variables

#do normal Make.mm stuff

# reset them back


PROJECT = vnf
PACKAGE = vnf

RECURSE_DIRS = \
    bin \
    cgi \
    config \
    content \
    html \
    log \
    vnf \


OTHERS = \

#--------------------------------------------------------------------------
#

all:
	BLD_ACTION="all" $(MM) recurse
	cp -r html/* /var/www/apache2-default

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $

# End of file
