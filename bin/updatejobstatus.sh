#!/usr/bin/env bash

./timer.py --command="./launch-detached.py -cmd=./updatejobstatus.py -home=`pwd`" -interval=10*second
