#!/usr/bin/env sh

#./timer.py --command="./runmonitors.sh `pwd`" -interval=10*minute &
./timer.py --command="./runmonitors.sh `pwd`" -interval=0.1*minute &
