.. _vnfdeveloperguideutilities:

Utilities
=========


User approval
-------------
To approve a user::

 $ cd $EXPORT_ROOT/vnfb/bin
 $ ./approveUser.py -username=<username>

Simply run approveUser without username will reload the
authentication service daemon.


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


Misc.
-----

Run a command in a subprocess and detach it from the current process
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

It is very useful in UI to launch a separate process that runs on its
own so we can get back to user quickly with a response. ::
 
 $ cd $EXPORT_ROOT/vnfb/bin
 $ ./launch-detached.py --home=<workdir> --cmd=<command> --output-log=<outputlogfile> --error-log=<errorlogfile>

You can get help by::

 $ ./launch-detached.py -h

Debugging::

 $ ./launch-detached.py <...options...> debug
