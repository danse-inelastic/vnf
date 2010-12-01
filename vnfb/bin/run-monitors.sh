#!/usr/bin/env sh

WORKDIR=$1

./launch-detached.py -cmd='./updatejobstatus.py --extension.ssher.known_hosts= --extension.ssher.private_key=' -home=$WORKDIR
./launch-detached.py -cmd='./checkservers.py --extension.ssher.known_hosts= --extension.ssher.private_key=' -home=$WORKDIR
