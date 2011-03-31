.. _vnfdeveloperguidedaemons:

Daemons
=======


A running VNF system is supported by a few daemons.
They are started by running ::

 $ start-luban-project.py /path/to/vnf/export/directory

Usually you don't need to deal with them, but it would be
useful to understand what they are.

journald.py
-----------
Logging.


idd.py
------
Global-unique id generation.


ipad.py
-------
Authentication service.

After changes user database, you will need to refresh ipad.
This can be done with the approveUser.py command::

 $ cd $EXPORT_ROOT/vnf/bin
 $ ./approveUser.py

