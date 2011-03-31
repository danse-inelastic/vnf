#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
QEConfiguration - table that holds task configuration records

Notes:
     (None)

TODO:
    - Change name from QEConfiguration to QEInput? QEInput is too specific?
"""

from vnf.components.QETable import QETable

class QEConfiguration(QETable):

    name = "qeconfigurations"
    import dsaw.db

    taskid    = dsaw.db.varchar(name="taskid", length=64)
    taskid.constraints = 'REFERENCES qetasks (id)'    # Important
    taskid.meta['tip'] = "Task id"

    # Later on can be tranformed to a separate File table
    filename    = dsaw.db.varchar(name="filename", length=1024, default='')
    filename.meta['tip'] = "Filename associated with this configuration"

    # To separate table?
    parser    = dsaw.db.varchar(name="parser", length=1024, default='')
    parser.meta['tip'] = "Parser for configuration"

    description = dsaw.db.varchar(name="description", length=1024, default='')
    description.meta['tip'] = "description"

    timecreated = dsaw.db.varchar(name="timecreated", length=32, default='')
    timecreated.meta['tip'] = "timecreated"

    timemodified = dsaw.db.varchar(name="timemodified", length=32, default='')
    timemodified.meta['tip'] = "timemodified"

    # Kind of redundant because QETask has also type
    type         = dsaw.db.varchar(name="type", length=1024, default='')
    type.meta['tip'] = "Configration type"


    # FIXME:
    # Question: Do I need text fields once I use get file from DDS location?
    # Answer: Keep it just in case
    text = dsaw.db.varchar(name="text", length=8192, default='')
    text.meta['tip'] = "text"


configPW = """ &control
    calculation='scf'
    restart_mode='from_scratch',
    tprnfor = .true.
    prefix='ni',
    pseudo_dir = '',
    outdir=''
 /
 &system
    ibrav=2,
    celldm(1) =6.65,
    nat=  1,
    ntyp= 1,
    nspin=2,
    starting_magnetization(1)=0.5,
    degauss=0.02,
    smearing='gauss',
    occupations='smearing',
    ecutwfc =27.0
    ecutrho =300.0
 /
 &electrons
    conv_thr =  1.0d-8
    mixing_beta = 0.7
 /
ATOMIC_SPECIES
 Ni  26.98  Ni.pbe-nd-rrkjus.UPF
ATOMIC_POSITIONS
 Ni 0.00 0.00 0.00
K_POINTS AUTOMATIC
4 4 4 1 1 1"""

configPH = """phonons of Ni at gamma
&inputph
  tr2_ph=1.0d-16,
  prefix='ni',
  ldisp=.true.,
  nq1=2,
  nq2=2,
  nq3=2,
  amass(1)=58.6934,
  outdir='',
  fildyn='ni.dyn',
/"""

configDOS = """&inputpp
   prefix='ni',
   outdir='',
   fildos='',
   Emin=5.0,
   Emax=25.0,
   DeltaE=0.1
/"""

configSettings  = """
[server]
server-name     = foxtrot.danse.us
num-proc        = 8
num-nodes    	= 8
proc-per-node 	= 12
npool       	= 8
executable      = mpirun
params          = --mca btl openib,sm,self
modules         = openmpi/gnu acml/4.3.0_gfortran64_int32 espresso
"""

# Electron DOS (Ni_E_DOS): taskid = 5

# Default records
defaults    = (
               {"id": 1, "taskid": 5, "type": "PW", "parser": "qeinput",
               "filename": "ni.scf.in", "text": configPW},
               {"id": 2, "taskid": 6, "type": "PH", "parser": "qeinput",
                "filename": "ni.ph.in", "text": configPH},
               {"id": 3, "taskid": 4, "type": "PP", "parser": "qeinput",
                "filename": "ni.pp.in", "text": configDOS},
                {"id": 4, "taskid": 5, "type": "DOS", "parser": "qeinput",
                "filename": "ni.scf.dos.in", "text": configDOS},
                {"id": 5, "taskid": 6, "type": "settings", "parser": "ConfigParser",   # Example of settings type
                "filename": "settings.conf", "text": configSettings},
              )

# Init tables
def inittable(clerk):
    for params in defaults:
        r   = QEConfiguration()
        r.setClerk(clerk)
        r.createRecord(params)


# Tests
def testDefaults():
    for e in defaults:
        s = ""
        for v in e.keys():
            s += "%s: %s " % (v, e[v])
        print s

def test():
    c   = QEConfiguration()
    print c.getColumnNames()

if __name__ == "__main__":
    testDefaults()
    test()

__date__ = "$Nov 24, 2009 5:49:56 PM$"


