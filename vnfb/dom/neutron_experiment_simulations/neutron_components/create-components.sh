#!/usr/bin/env bash

./mcstas-component-to-dom.py  -type=IQE_monitor -category=monitors --base=Monitor --tablebase=MonitorTableBase --newname=QEMonitor --skip-props=filename
#./mcstas-component-to-dom.py  -type=E_monitor -category=monitors --base=Monitor --tablebase=MonitorTableBase --newname=EMonitor --skip-props=filename
#./mcstas-component-to-dom.py  -type=L_monitor -category=monitors --base=Monitor --tablebase=MonitorTableBase --newname=LMonitor --skip-props=filename
#./mcstas-component-to-dom.py  -type=TOF_monitor2 -category=monitors --base=Monitor --tablebase=MonitorTableBase --newname=TofMonitor --skip-props=filename
#./mcstas-component-to-dom.py  -type=Q_monitor -category=monitors --base=Monitor --tablebase=MonitorTableBase --newname=QMonitor --skip-props=filename
#./mcstas-component-to-dom.py  -type=PSD_monitor_4PI -category=monitors --base=Monitor --tablebase=MonitorTableBase --newname=SphericalPSD --skip-props=filename
#./mcstas-component-to-dom.py  -type=VulcanDetectorSystem -category=monitors --base=Monitor --tablebase=MonitorTableBase --newname=VulcanDetectorSystem --skip-props=filename

./mcstas-component-to-dom.py  -type=Channeled_guide -category=obsolete --newname=ChanneledGuide
./mcstas-component-to-dom.py  -type=Fermi_chop2 -category=optics --newname=FermiChopper --skip-props=max_iter
./mcstas-component-to-dom.py  -type=Vertical_T0 -category=optics --newname=T0Chopper



#./mcstas-component-to-dom.py  -type=SNS_source_r1 -category=sources --newname=SNSModerator
