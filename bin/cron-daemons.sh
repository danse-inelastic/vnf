#!/usr/bin/env sh
spawn-daemon.py  -cmd='./timer.py --command="./run-daemons.sh `pwd`" -interval=60*minute' -home=.
