#!/usr/bin/env bash
releaser=/home/vnf/dv/danse/buildInelast/web-vnf-alpha
EXPORT_ROOT=$releaser/EXPORT
source $EXPORT_ROOT/bin/envs.sh
cd $EXPORT_ROOT/vnf/cgi && python main.py $@
