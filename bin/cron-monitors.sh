#!/usr/bin/env sh
spawn-daemon.py  -cmd='./timer.py --command="./run-monitors.sh `pwd`" -interval=10*minute' -home=. 
