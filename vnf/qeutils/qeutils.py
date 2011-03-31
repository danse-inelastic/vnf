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
Contains little but useful itils!
"""
import os.path

import os
import re
from vnf.qeutils.qeconst import INPUT, INPUT_DEFAULT, ANALYSIS, SUBTYPE_MATDYN, SIMTYPE, SIMCHAINS
from vnf.qeutils.qescheduler import schedulerfactory
from vnf.qeutils.qeparser.qeinput import QEInput
import luban.content as lc
from luban.content import load, select

# Issue: number of columns depends on magnetism of the material
#   Margetic:       (e, up, down, cum)
#   Non-magnetic:   (e, dos, cum)
def parseElectronDos(filename):
    """Parses file consisting of at least 4 columns separated by space or tab
    Notes:
        - First line is the description
    """
    e = []
    x = []
    y = []
    z = []
    f = open(filename,  "r")
    line = f.readline() # Skip the first line with header
    line = f.readline()
    while line:
        list = line.split()

        #Convert strings to float and append to the list
        e.append(float(list[0]))
        x.append(float(list[1]))
        y.append(float(list[2]))
#        z.append(float(list[3]))
        line = f.readline()
    f.close()
    return (e,  x,  y)
#    return (e,  x,  y,  z)


def parsePhononDos(filename):
    if not os.path.exists(filename):
        return None
    
    e = []
    x = []
    f = open(filename,  "r")
    line = f.readline()
    while line:
        list = line.split()
        #print list
        e.append(float(list[0]))
        x.append(float(list[1]))
        line = f.readline()
    f.close()
    return (e,  x)


def parseVDos(filename):
    """Parses file consisting of 2 columns separated by space or tab
    to parse vibrational dos
    Notes:
        - First line is the description
    """
    e = []
    x = []

    f = open(filename)
    line = f.readline() # Skip the first line with header
    line = f.readline()
    while line:
        list = line.split()
        #Convert strings to float and append to the list
        e.append(float(list[0]))
        x.append(float(list[1]))
        line = f.readline()
    f.close()
    return (e,  x)

def newid(director):
    "Id generator "
    id  = ''
    if director:
        id = director.getGUID()     # Changed from idd.token().locator

    return id


def timestamp():
    """Returns time stamp"""
    import time
    return int(time.time())

"""Replaces ternary operator in C: '?:' (e.g. a ? a: 4) """
ifelse  = lambda a,b,c: (b,c)[not a]

"""
Sets attribute 'name' of object 'obj' from params dictionary
Used mostly on database classes (vnf.dom)
"""
setname = lambda params, obj, name: ifelse(params.has_key(name), params.get(name), getattr(obj, name))


def fstr(num):
    "Takes float number and returns formated string"
    return "%# .2f" % num   # use "%.2f" instead?


def stamp2date(stamp):
    """Converts stamp to date"""
    import time
    import re
    p   = re.compile("[\d.]+")
    m   = p.match(str(stamp))
    
    if m:   # Check if timestamp
        return time.strftime("%b %d %Y, %H:%M:%S", time.localtime(float(stamp)))

    return ""


def stamp():
    "Returns timestamp"
    import time
    return time.time()


def makedirs(path):
    "Recursively creates directory specified by path"
    import os
    if not os.path.exists(path):
        os.makedirs(path)


def writeFile(filename, content):
    "Write content to file"
    if not content:     # If content is None, set it to empty
        content = ""    
        
    # Removes carriage return (for conig files generated in Windows)
    p           = re.compile("\r")

    filtered    = p.sub("", content)
    open(filename, 'w').write(filtered)


def writeRecordFile(dds, record, fname, content):
    "Writes content to file which location specified by the record"
    path        = dds.abspath(record)
    absfilename = dds.abspath(record, filename = fname)
    makedirs(path)      # Create directory is does not exist
    writeFile(absfilename, content)


def readFile(filename):
    "Read content of the file from absolute filename"
    if os.path.exists(filename):
        return open(filename).read()
    
    return None


def recordFileExists(dds, record, fname):
    absfilename = dds.abspath(record, filename = fname)
    return os.path.exists(absfilename)


def defaultInputName(type):
    t   = type.lower()
    if t in INPUT.keys():
        return INPUT[t]

    return INPUT_DEFAULT


# XXX: Check if record has "type" attribute
def readRecordFile(dds, record, fname=None):
    "Writes content to file which location specified by the record"
#    if not fname:   #and record has attribute "type"
#        fname   = defaultInputName[getattr(record, "type")]
        
    absfilename = dds.abspath(record, filename = fname)
    return readFile(absfilename)


def dataroot(director, relative = False):
    "Returns data root directory where the simulation results are exported"
    # Example:
    #    relative = False: "/home/dexity/exports/vnf/vnf/content/data"
    #    relative = True:  "../content/data"

    if not director:
        return None
    
    dds = director.dds
    if relative:
        return dds.dataroot
    
    return os.path.abspath(dds.dataroot)



def packname(id, name):
    """Packs name by appending name to id.
    E.g.
        id   = "3YEQ8PNV"
        name = "ni.scf.in"
    =>  3YEQ8PNVni.scf.in
    """
    return "%s%s" % (id, name)

def unpackname(string, id):
    """
    Unpacks string: returns tupple (id, name) by trancating id from string
    """
    parts   = string.split("id")
    
    # raise error if id is not in string
    assert len(parts) == 2  # breaks into two parts
    assert parts[0] == ''
    name    = parts[1]

    return (id, name)


def key2str(key):
    "Takes key in form, like 'create-job' and returns 'Create job'"
    # words are separated by "-" character
    return " ".join(key.split("-")).capitalize()


def key2val(key, dict, default=""):
    "Returns value specified by key, or default - otherwise"
    if key in dict.keys():
        return dict[key]

    return default


def selection2typekey(selection):
    "Returns key of simulation type based on selection"
    # Example: 
    #   Input: 6
    #   Output: "molecular-dynamics"
    keys        = SIMTYPE.keys()
    selected    = int(selection)
    if not selected in range(len(keys)):
        return ""

    return keys[selected]


def label2typekey(label):
    "Returns key of simulation type from label"
    # Example:
    #   Input: "Molecular Dynamics"
    #   Output: "molecular-dynamics"
    for type in SIMTYPE.keys():
        if SIMTYPE[type] == label:
            return type

    return ""


def simChain(csvstr):
    "Takes comma-separated value and returns list"
    if not csvstr:
        return ()
    list    = csvstr.split(",")
    for i in range(len(list)):
        list[i] = list[i].strip()   # In case if there are spaces
        
    return list


def nonMDChain(typekey):
    "Returns non-molecular dynamics chain from qeconst.py"
    # Example:
    #   Input: "electron-dos"
    #   Output: "PW,PW,DOS"
    if typekey == "":   # Empty typekey
        return ""
    chain   = SIMCHAINS[SIMTYPE[typekey]]   # list
    s   = ""
    for c in chain:
        s   += "%s," % c    # Create simulation chain string

    s   = s.rstrip(",")
    return s


def noHyphen(str):
    "Removes hyphen from a string"
    # Example:
    #   Input: "hello-world"
    #   Output: "helloworld"
    HYPHEN  = "-"
    list    = str.split(HYPHEN)
    s       = ""
    for l in list:
        s   += l

    return s


def latestRecord(records, timefield):
    """Retruns latest record based on timefield column
        timefield   - string
    """
    if len(records) == 0:
        return None

    # Jobs should have at least one element
    latest  = records[0]

    for r in records:
        if getattr(r, timefield) == "":
            continue

        if getattr(latest, timefield) == "":
            latest = r

        if float(getattr(r, timefield)) > float(getattr(latest, timefield)):
            latest  = r

    return latest


# Refactor to a more general function?
def latestJob(jobs):
    "Retruns latest job based on timesubmitted column"
    return latestRecord(jobs, "timesubmitted")


def latestTask(tasks):
    return latestRecord(tasks, "timecreated")


def latestInput(inputs):
    return latestRecord(inputs, "timecreated")


def latestParam(params):
    return latestRecord(params, "timecreated")


def getResult(director, id, sim, linkorder):
    "Returns result object specified by parameters"
    if not sim or not director or linkorder < 0:     # No simulation object, no result
        return None

    assert sim.id   == id
    if not sim.type in SIMCHAINS.keys():
        return None     # Don't recognize simulatin type

    if linkorder >= len(SIMCHAINS[sim.type]):       # Exceed number of tasks
        return None

    tasktype    = SIMCHAINS[sim.type][linkorder]    # Get the task type
    assert type(tasktype) == str
    modfile     = tasktype.lower()+"result"
    modclass    = tasktype.upper()+"Result"
    module      = _import("vnf.qeutils.results.%s" % modfile)
    # from vnf.qeutils.results.phresult import PHResult
    result      = getattr(module, modclass)(director, id)   # instance
    return result


simTask = {
            "simulationid":     "getQESimulationTasks",
            "convparamid":      "getQEConvParamTasks"
          }

def qetask(director, simid, linkorder, subtype = None, refid = "simulationid"):
    "Returns task object specified by simulation id and linkorder"
    if not refid in simTask.keys(): # Don't understand refid
        return None
    
    where   = "%s='%s'" % (refid, simid)
    if subtype:
        where   += "%s AND subtype='%s'" % (where, subtype)
    simtasks = getattr(director.clerk, simTask[refid])(where=where)
    for st in simtasks:
        tasks   = director.clerk.getQETasks(where="id='%s' AND linkorder=%s" % (st.taskid, linkorder))
        if tasks:   # XXX First found tasks
            break

    if tasks:
        return latestTask(tasks)

    return None


def qejob(director, simid, linkorder, subtype = None, refid = "simulationid"):
    """Return latest job for the linkorder
    For matdyn task subtype will be also used which can be "dos" or "dispersion".
    The subtype uses QETask.short_description (should be removed from) and QEJob.description to store
    the subtype"""
    task    = qetask(director, simid, linkorder, refid = refid) # Let's not use 'subtype' for qetask()
    if task:
        where   = "taskid='%s'" % task.id
        if subtype:
            where   = "%s AND description='%s'" % (where, subtype)
        jobs    = director.clerk.getQEJobs(where=where)
        return latestJob(jobs)
    
    return None


def qeinput(director, simid, linkorder, refid = "simulationid"):
    "Return input for the linkorder"
    task    = qetask(director, simid, linkorder, refid = refid)
    if task:
        inputs  = director.clerk.getQEConfigurations(where="taskid='%s'" % task.id)
        return latestInput(inputs)  # There should be a single input record!

    return None


def torqueFactory(director, job, server):
    "Set up torque and return object"
    if not director or not job or not server:   # If one of them is None return None
        return None

    factory = schedulerfactory(server)    # vnf.clusterscheduler.qetorque.Scheduler
    jobpath = director.dds.abspath(job, server=server)
    launch  = lambda cmd: director.csaccessor.execute(
                                                    cmd,
                                                    server,
                                                    jobpath,
                                                    suppressException = True)

    return factory(launch)


def deleteJob(director, job, server):
    "Deletes job on the server"
    torque  = torqueFactory(director, job, server)
    if not torque:
        return None

    try:
        result  = torque.delete(torque.jobId())
    except:
        return None

    return result


def jobStatus(director, job, server):
    "Returns job status on the remote cluster"
    torque  = torqueFactory(director, job, server)
    if not torque:
        return None

    try:
        status  = torque.status(torque.jobId())
    except:
        return None

    return status


def analyseActor(simtype):
    "Returns analysis actor based on simulation type"
    name    = "default"

    if simtype in ANALYSIS.keys():
        name    = ANALYSIS[simtype]

    return 'material_simulations/espresso-analysis/%s' % name


def qedialog(title, text, Class="qe-dialog-output"):
    "Returns the dialog widget"
    dialog  = lc.dialog(title=title, autoopen=True, Class=Class)
    dialog.add(text)   # Text
    okbutton = lc.button( label     = 'OK',
                          onclick   = select(element=dialog).destroy())
    dialog.add(okbutton)
    return dialog
    

def setInputParam(text, param, value):
    "Gets input string, sets param value and returns updated string"
    # XXX: Parameters should be from "SYSTEM" namelist (extend for K-points)
    input   = QEInput(config=text)
    input.parse()
    nl      = input.namelist("system")
    nl.set(param, value)
    return input.toString()


def getInputParam(text, param):
    "Gets input string, sets param value and returns updated string"
    # XXX: Parameters should be from "SYSTEM" namelist (extend for K-points)
    input   = QEInput(config=text)
    input.parse()
    nl      = input.namelist("system")
    return nl.param(param)

# Subtype is relevant for matdyn mostly. So I don't care about other types
def subtypeMatdyn(subtype):
    if subtype == "":
        return ""   # Empty subtype

    subtype = int(subtype)  # Convert to integer, if possible
    if not subtype in range(len(SUBTYPE_MATDYN)):
        return ""   # subtype is out of range

    return SUBTYPE_MATDYN[subtype]


CONV_JOB_BASE       = "convjob"
CONV_JOB_ROW_BASE   = "convjob-row"

def convJobId(row, col):
    return "%s-%s-%s" % (CONV_JOB_BASE, row, col)

def convJobRowId(row):
    return "%s-%s" % (CONV_JOB_ROW_BASE, row)


def serverName(address):
    """
    Takes server address and returns short name

    Example:
        foxtrot.danse.us -> foxtrot
    """
    default = ""
    if not address:
        return default

    parts   = address.split(".")
    if len(parts) > 0:
        return parts[0]

    return default


def _import(package):
    return __import__(package, globals(), locals(), [''], -1)


# *********** TESTS ******************************

def testStamp():
    import time
    print stamp2date(time.time())


if __name__ == "__main__":
    testStamp()

__date__ = "$Jul 30, 2009 12:08:31 PM$"
