#!/usr/bin/env sh

WORKDIR=$1

./launch-detached.py -cmd='./updatejobstatus.py' -home=$WORKDIR
./launch-detached.py -cmd='./checkservers.py' -home=$WORKDIR
