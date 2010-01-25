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
from vnfb.utils.qeresults import QEResults
from vnfb.utils.qetaskinfo import TaskInfo


def parseFile(filename):
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
        z.append(float(list[3]))
        line = f.readline()
    f.close()
    return (e,  x,  y,  z)


def parsePHFile(filename):
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
Used mostly on database classes (vnfb.dom)
"""
setname = lambda params, obj, name: ifelse(params.has_key(name), params.get(name), getattr(obj, name))


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
    """Recursively creates directory specified by path"""
    import os
    if not os.path.exists(path):
        os.makedirs(path)


def writefile(filename, content):
    open(filename, 'w').write(content)


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


def latestJob(jobs):
    "Retruns latest job based on timesubmitted column"
    return latestRecord(jobs, "timesubmitted")


def latestTask(tasks):
    return latestRecord(tasks, "date")


def latestInput(inputs):
    return latestRecord(inputs, "timecreated")

# Includes *hack* by using short_description field for subtype
def qetask(director, simid, type, subtype = None):
    "Returns task object defined by simulation id and type"
    where   = "simulationid='%s'" % simid
    if subtype:
        where   += "%s AND short_description='%s'" % (where, subtype)
    simtasks = director.clerk.getQESimulationTasks(where=where)
    for st in simtasks:
        tasks   = director.clerk.getQETasks(where="id='%s' AND type='%s'" % (st.taskid, type))
        if tasks:   # XXX First found tasks
            break

    if tasks:
        return latestTask(tasks)

    return None


def qejob(director, simid, type, subtype = None):
    "Return latest job for the type"
    task    = qetask(director, simid, type) # Let's not use 'subtype' for qetask()
    if task:
        where   = "taskid='%s'" % task.id
        if subtype:
            where   = "%s AND description='%s'" % (where, subtype)
        jobs    = director.clerk.getQEJobs(where=where)
        return latestJob(jobs)
    
    return None


def qeinput(director, simid, type):
    "Return input for the type"
    task    = qetask(director, simid, type)
    if task:
        inputs  = director.clerk.getQEConfigurations(where="taskid='%s'" % task.id)
        return latestInput(inputs)  # There should be a single input record!

    return None


def resultsdir(director, simid, type, subtype = None):
    "Returns results directory in data/tmp"    
    job     = qejob(director, simid, type, subtype)
    if job:
        dds         = director.dds
        dataroot    = os.path.abspath(dds.dataroot)
        taskinfo    = TaskInfo(simid = simid, type = type)
        results     = QEResults(director, job, taskinfo)
        if results.ready():
            return os.path.join(dataroot, results.tardir())

    return None


# TODO: Test!!!
def remoteResultsPath(director, simid, type):
    """Returns the path of the jobs directory specified by simulation id (simid) and task type.
    Example: /home/dexity/espresso/qejobs/5YWWTCQT/
    """
    path    = ""
    task    = qetask(director, simid, type)

    if not task:
        return path

    jobs    = director.clerk.getQEJobs(where="taskid='%s'" % task.id)
    if len(jobs) > 0:
        # Find latest job for the task
        job = latestJob(jobs)

        if job:
            server  = director.clerk.getServers(id=job.serverid)
            path    = os.path.join(server.workdir, job.name)
            path    = os.path.join(path, job.id)

    return path


def inputRecord(director, simid, type):
    task    = qetask(director, simid, type)

    if not task:
        return None

    inputs  = director.clerk.getQEConfigurations(where="taskid='%s'" % task.id)
    if len(inputs) > 0:
        # Should be one config input for the task!
        return inputs[0]

    return None


# *********** TESTS ******************************

def testStamp():
    import time
    print stamp2date(time.time())


if __name__ == "__main__":
    testStamp()

__date__ = "$Jul 30, 2009 12:08:31 PM$"


# ********************* DEAD CODE ***************************

#    simtasks = director.clerk.getQESimulationTasks(where="simulationid='%s'" % simid)
#    for st in simtasks:
#        tasks   = director.clerk.getQETasks(where="id='%s' AND type='%s'" % (st.taskid, type))
#        if tasks:   # XXX First found tasks
#            break
#
#    if not tasks:
#        return path
#
#    task    = latestTask(tasks)    # task    = tasks[0]
#    if not task:
#        return path

