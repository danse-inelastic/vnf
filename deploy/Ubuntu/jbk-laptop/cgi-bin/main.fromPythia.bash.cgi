#!/usr/bin/env bash
releaser=/home/jbk/DANSE/buildInelast/pyre
EXPORT_ROOT=$releaser/EXPORT
source $EXPORT_ROOT/bin/envs.sh
cd $EXPORT_ROOT/vnf/cgi && python main.py $@
