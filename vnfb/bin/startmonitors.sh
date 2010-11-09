#!/usr/bin/env sh
spawn-daemon.py  -cmd='./timer.py --command="./runmonitors.sh `pwd`" -interval=10*minute' -home=. 
