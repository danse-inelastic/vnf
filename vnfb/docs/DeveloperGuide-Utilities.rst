.. _vnfdeveloperguideutilities:

Utilities
=========


System monitors
---------------
VNF is a complex system that needs constant monitoring of system
health and system status. This is done by periodically running
scripts, each of which working on one aspect of the system.

Several scripts exist in $EXPORT_ROOT/vnfb/bin to do this job:

* startmonitors.sh: script that periodically calls script
  "runmonitors.sh"
* runmonitors.sh: script that runs monitor scripts

The startmonitors.sh calls "timer.py" to periodically run a
script (s). (This could be replaced by cron jobs.)

The runmonitors.sh script has the following main content::

 ./launch-detached.py -cmd='./updatejobstatus.py' -home=$WORKDIR
 ./launch-detached.py -cmd='./checkservers.py' -home=$WORKDIR
 ...

Each line looks like this::

 ./launch-detached.py -cmd=<cmd> -home=$WORKDIR

The launch-detached.py script is responsible to launch the command
<cmd> to a separate process so that the running of the command does
not block the script. Each command <cmd> is a regular command that
does something. For example, command "checkservers.py" check the 
computing servers to see if they are working correctly.


Communication
-------------

Make an email announcement
""""""""""""""""""""""""""

To send an email announcement, use method
vnfb.utils.communications.announce.

Example::

 >>> from vnfb.utils.communications import announce
 >>> announcement = 'bug-report'
 >>> announce(director, announcement, user, bugid, comment, traceback)

.. note::
   Method "announce" is actually just a shortcut to use an
   announcement component. 
   You could use an announcement component directly if you prefer.

The signature of the announce method depends on the anncoucement
component. The parameter "anncoucement" of the method "announce"
is a string, and is used to look up the announcement component.
In the example code piece above, "bug-report" is the announcement
component name. So the component
`"content/components/announcements/bug-report.odb" <http://danse.us/trac/VNET/browser/vnf/branches/beta-useluban/vnfb/content/components/announcements/bug-report.odb>`_
will be used, and the parameters after the "announcement"
parameter in the call to function "announce" 
(here, they are "user", "bugid", "comment", and "traceback")
are passed
to the component factory method 
(`method definition is here <http://danse.us/trac/VNET/browser/vnf/branches/beta-useluban/vnfb/content/components/announcements/bug-report.odb#L13>`_)::

 def announcement(user, bugid, comment, traceback):
     ...
     ...


