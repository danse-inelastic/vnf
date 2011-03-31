#!/usr/bin/env python

# Adapted by Nikolay Markovskiy, Alex Dementsov

from nMOLDYN.Analysis.Template import CartesianDensityOfStates_serial
from MMTK.Trajectory import Trajectory
from Scientific import N
import sys
import getopt

def usage():
   print """Available options:
 -f <filename> or --filename=gulpOutputFilename(default=pout)
 -b <start>    or --begin=starting element(default=0)
 -s <step>     or --step=integer increment(default=1)
 -e <end>      or --end=last element of trajectory(default=len(trajectory)-1)
 -t <T,K>      or --temperature=T
"""

TR_PATH = "si64.nc"

if __name__ == "__main__":

   temperature = 300.0

   # Defaults:
   begin = 0
   end = -1
   step = 1
   trajectoryPath = TR_PATH

   try:
       opts, args = getopt.getopt(sys.argv[1:], "hf:b:e:s:t:", ["help","filename=","begin=","step=","end=","temperature="])
   except getopt.GetoptError:
       usage()
       sys.exit(2)
   for opt, arg in opts:
       if opt in ("-b", "--begin"):
           begin = int(arg)
       if opt in ("-e", "--end"):
           end = int(arg)
       if opt in ("-s", "--step"):
           step = int(arg)
       if opt in ("-h", "--help"):
           usage()
           sys.exit(2)
       if opt in ("-f", "--filename"):
           trajectoryPath = arg
       if opt in ("-t", "--temperature"):
           temperature = float(arg)

   print "Using file %s as input..."%trajectoryPath


   trajectory = Trajectory(None, trajectoryPath, 'r')

   if end == -1:
       end = len(trajectory.time)

   timeinfo =  '%d:%d:%d'%(begin, end, step)
   print 'The complete trajectory size is', len(trajectory.time), ' elements'
   print "\nAnalysing trajectory from position %d to postion %d with step %d:\n"%(begin,end,step)
   print 'Temperature = ',temperature

#    print (trajectory.time[0], trajectory.time[-1], trajectory.time[1] - trajectory.time[0])

   parameters = {
                   'trajectory': trajectory,
                   'timeinfo'  : timeinfo,
                   'differentiation': 0,
                   'projection': 'no',
                   'fftwindow' :    10.0,
                   'subset': 'all',
                   'deuteration': 'no',
                   'weights': 'equal',
                   'dos': 'dos.nc',
                   'pyroserver': 'monoprocessor',

   }

   dos = CartesianDensityOfStates_serial( parameters = parameters, statusBar = None)
   dos.runAnalysis()

   # 'freqencies' = 1D Numeric array. Frequencies at which the DOS was computed
   frequencies = N.arange(dos.nFrames)/(2.0*dos.nFrames*dos.dt)
 #   print dos.dt
 #   print dos.nFrames

   DOS = dos.DOS/dos.DOS.sum()#/(frequencies[1] - frequencies[0])

   s = ''
   for f, g in zip(frequencies, DOS):
       s = s + '%f    %f\n'%(f, g)
   open('dos.txt', 'w').write(s)

   KelvinToTeraHz = 0.0208614368624
   TeraHzToKelvin = 47.935336697834

   #print frequencies
   # print dos.DOS.sum()
#*(frequencies[1] - frequencies[0])


   import numpy

   #from enfit import entropyEstimator
   #from enfit import Lorentzian
   #from enfit import Gaussian

#    print entropyEstimator(Q = 5, broadeningFunction = Gaussian, temperature = 550, g_orig = DOS[1:], frequencies = frequencies[1:])



   arg = frequencies[1:]/temperature/KelvinToTeraHz
   exponent = numpy.exp(arg)

   F = temperature*( 0.5*arg + numpy.log(1.0 - 1.0/exponent ))*DOS[1:]
   print 'Free Energy: ', F.sum()

   n = 1.0/(exponent - 1.0)
   s_osc =  (1.0 + n[:])*numpy.log(1.0 + n[:]) - n[:]*numpy.log(n[:])
   entropy1 = (DOS[1:]*(numpy.log(temperature*KelvinToTeraHz/frequencies[1:])+1.0)).sum()#*( frequencies[1] - frequencies[0] )
   entropy2 = (DOS[1:]*s_osc).sum()#*( frequencies[1] - frequencies[0] )
   print 'entropy = ', entropy2
