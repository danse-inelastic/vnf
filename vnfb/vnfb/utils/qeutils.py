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

import os

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


# TODO: Test!!!
def remoteResultsPath(director, simid, type):
    """Returns the path of the jobs directory specified by simulation id (simid) and task type.
    Example: /home/dexity/espresso/qejobs/5YWWTCQT/
    """
    path    = ""
    simtasks = director.clerk.getQESimulationTasks(where="simulationid='%s'" % simid)
    for st in simtasks:
        tasks   = director.clerk.getQETasks(where="id='%s' AND type='%s'" % (st.taskid, type))
        if tasks:   # XXX First found tasks
            break

    if not tasks:
        return path

    task    = latestTask(tasks)    # task    = tasks[0]
    if not task:
        return path

    jobs    = director.clerk.getQEJobs(where="taskid='%s'" % task.id)
    if len(jobs) > 0:
        # Find job of Q2R task
        job = latestJob(jobs)

        if job:
            server  = director.clerk.getServers(id=job.serverid)
            path    = os.path.join(server.workdir, job.name)
            path    = os.path.join(path, job.id)

    return path
    


# *********** TESTS ******************************

def testStamp():
    import time
    print stamp2date(time.time())


if __name__ == "__main__":
    testStamp()

__date__ = "$Jul 30, 2009 12:08:31 PM$"


