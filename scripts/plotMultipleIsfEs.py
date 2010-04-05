"""This script allows one to create and plot a series of S(E)s.  
It is made for incoherent scattering from hydrogen in KC24."""
import os
from vsat.Trajectory import Trajectory as MdTrajectory
from vsat.trajectory.IsfCalc import IsfCalc
from plotlib.NcPlottableSet import NcPlottableSet
import numpy as np

temps = [2,3,5,10,15,20,25,30,40,50,60,70]
temps = [5,10,20,30,40,50,60,70,80]
#temps = []
sqeFiles=[]
base = 'sup8x4temp'
for temp in map(str,temps):
    #convert trajectory
    rawTraject = base+temp+'.his'
    ncFile = base+temp+'.nc'
    try: os.stat(ncFile)
    except:
        cmd = 'postProcessGulp.py --convertHistoryFile=True --historyFile='+rawTraject+' --ncFile='+ncFile 
        #temp sub for job submission
        os.system(cmd)
    #create the S(Q,E)s 
    traj = MdTrajectory(trajectoryPath=ncFile)   
    isfc = IsfCalc()
    isfc.q_range_iso = [2.3, 10]
    isfc.trajectory = traj
    #isfc.time_steps_sampled = (0, 41400, 414) # MdPlan(0.5, 0.01, 0.01)
    #isfc.time_steps_sampled = (5000, 9137, 21) # MdPlan(10, 0.1, 0.01)
    isfc.time_steps_sampled = (1000, 9268, 52) # MdPlan(4, 0.05, 0.01)
    isfc.selected_atoms = "{'deuterium': ['*']}"
    isfc.writeInputFile()
    isfFile = isfc.sqeFile
    try: os.stat(isfFile)
    except:
        import parnasisApp
        parnasisApp.main({'--isf':'','--input':'isf.inp'})
        #os.system('parnasisApp.py --csf --inp csf.inp')
    sqeFiles.append(isfFile)

    
#now create plot with all temps
ncPlottables = NcPlottableSet(sqeFiles, removeElasticLine = True)
ncPlottables.plot(sumQs=True)

    