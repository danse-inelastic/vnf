#!/bin/env bash

dest='/home/danse-vnf-admin/vnf/data/qejobs/82KTLTR'

epsc3path=`which epsc3`
cp $epsc3path $dest
cd $dest
./epsc3 > EPSC.out