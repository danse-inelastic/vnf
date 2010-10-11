#!/usr/bin/env sh
ipad.py --home=../config --stop
spawn-daemon.py  -cmd='./timer.py --command="./runmonitors.sh `pwd`" -interval=10*minute' -home=.  -stop