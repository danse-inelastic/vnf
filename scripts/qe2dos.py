#!/usr/bin/env python

# Adapted by Alex Dementsov, Nikolay Markovskiy

# NOTE:
#   - This is hardcoded version for Si 64
#   - XXX: Generalize

# See also:
#   http://dev.danse.us/trac/common/browser/kernelGenerator/src/vsat/trajectory/ConvertFromGulpDLPOLY.py

import string
import numpy
from Scientific import N
from MMTK import *
from MMTK.Trajectory import Trajectory, SnapshotGenerator, TrajectoryOutput
from nMOLDYN.Analysis.Template import CartesianDensityOfStates_serial


SPECIES     = [['Si',64,[('si','Si')],[]], ]
VELFILE     = 'cp.vel'
POSFILE     = 'cp.pos'
NCFILE      = 'cp.nc'
DOSFILE     = "vdos.dos"
OUTPUT      = "output.in.out"
N_VECTORS   = 2
PBC         = 3
BOX_X       = 20.52
BOX_Y       = 20.52
BOX_Z       = 20.52
DT          = 0.024189  # 100*10.0 a.u. (dt = 10.0) # 0.00120944
N_ATOMS     = 64

TEMPERATURE     = 300.0
KelvinToTeraHz  = 0.0208614368624
TeraHzToKelvin  = 47.935336697834


class QEData:

    def __init__(self):
        self.title      = "Generated from CP of Quantum Espresso"
        self.velfile    = open(VELFILE)
        self.posfile    = open(POSFILE)

        self.makeUniverse(PBC, SPECIES)
        self.universe.initializeVelocitiesToTemperature(0.)


    def makeUniverse(self, pbc, molecules):
        if pbc == 0:
            self.universe = InfiniteUniverse()
        else:
            self.universe = OrthorhombicPeriodicUniverse((0., 0., 0.))
        number = 0
        for mol_name, mol_count, atoms, constraints in molecules:
            for i in range(mol_count):
                atom_objects = []
                for element, name in atoms:
                    a = Atom(element, name = name)
                    a.number = number
                    number = number + 1
                    atom_objects.append(a)
                if len(atom_objects) == 1:
                    self.universe.addObject(atom_objects[0])
                else:
                    ac = AtomCluster(atom_objects, name = mol_name)
                    for i1, i2, d in constraints:
                        ac.addDistanceConstraint(atom_objects[i1],
                                                 atom_objects[i2],
                                                 d)
                    self.universe.addObject(ac)
        self.universe.configuration()


    def writeTrajectory(self, trajectory_name, block_size=1):
        trajectory  = Trajectory(self.universe, trajectory_name, 'w',
                                self.title, block_size=block_size)
        actions     = [TrajectoryOutput(trajectory, ["all"], 0, None, 1)]
        snapshot    = SnapshotGenerator(self.universe, actions=actions)
        conf        = self.universe.configuration()
        vel         = self.universe.velocities()
        grad        = ParticleVector(self.universe)
        nvectors    = N_VECTORS
        natoms      = N_ATOMS
        self._setSize()

        try:
            while True:
                vline   = self.velfile.readline()
                pline   = self.posfile.readline()
                if not vline:
                    break

                vdata   = vline.split()
                pdata   = pline.split()

                if len(pdata) == 2: # Example: ["10", "0.00120944"]
                    step        = int(vdata[0])
                    step_data   = {'time': step*DT}

                for i in range(natoms):
                    conf.array[i]   = map(float, string.split(self.posfile.readline()))
                    vel.array[i]    = map(float, string.split(self.velfile.readline()))

                conf.array = Units.Ang*conf.array
                if nvectors > 1:
                    vel.array = Units.Ang/Units.ps * vel.array

                snapshot(data=step_data)
        finally:
            trajectory.close()


    def _setSize(self):
        "Set universe size"
        box_x = BOX_X*Units.Ang
        box_y = BOX_Y*Units.Ang
        box_z = BOX_Z*Units.Ang
        self.universe.setSize((box_x, box_y, box_z))



def generateDos():
    "Generates DOS"
    temperature = TEMPERATURE

    # Defaults:
    begin = 0
    end = -1
    step = 1
    trajectoryPath = NCFILE

    log     = ""    # Starting log
    log     += "Using file %s as input...\n" % trajectoryPath

    trajectory = Trajectory(None, trajectoryPath, 'r')

    if end == -1:
       end = len(trajectory.time)

    timeinfo =  '%d:%d:%d' % (begin, end, step)
    log     += 'The complete trajectory size is %d elements\n' % len(trajectory.time)
    log     += "\nAnalysing trajectory from position %d to postion %d with step %d:\n" % (begin, end, step)
    log     += 'Temperature = %s\n' % temperature

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
    frequencies = N.arange(dos.nFrames)/(2.0*dos.nFrames*dos.dt)

    DOS = dos.DOS/dos.DOS.sum()

    s = ''
    for f, g in zip(frequencies, DOS):
       s    += '%f    %f\n' % (f, g)
    open(DOSFILE, 'w').write(s)

    arg = frequencies[1:]/temperature/KelvinToTeraHz
    exponent = numpy.exp(arg)

    F = temperature*( 0.5*arg + numpy.log(1.0 - 1.0/exponent ))*DOS[1:]
    log     += 'Free Energy: %s\n' % F.sum()

    n = 1.0/(exponent - 1.0)
    s_osc =  (1.0 + n[:])*numpy.log(1.0 + n[:]) - n[:]*numpy.log(n[:])
    entropy1 = (DOS[1:]*(numpy.log(temperature*KelvinToTeraHz/frequencies[1:])+1.0)).sum()
    entropy2 = (DOS[1:]*s_osc).sum()
    log     += 'entropy = %s\n' % entropy2

    open(OUTPUT, 'w').write(log)    # Store log to output file


if __name__ == "__main__":
    data = QEData()
    data.writeTrajectory(NCFILE)

    generateDos()

__date__ = "$May 17, 2010 9:31:55 PM$"



