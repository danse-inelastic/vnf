#!/usr/bin/env sh
ipad.py --config=/tmp/luban-services,../config --- --home=../config
spawn-daemon.py  -cmd='./timer.py --command="./runmonitors.sh `pwd`" -interval=10*minute' -home=. 