.. _vnfdeveloperguideaccesscontrol:

Access control
==============

database design
---------------

.. image:: images/developerguide/accesscontrol/dbdesign.png
   :width: 720px

A user can have roles.

A role can have roles.

A role can have privileges.

A privilege may qualitfy a role to perform some actions.

Example ::

  User jbrkeith has a role of vnf/core-developer
  The role vnf/core-developer is in the "group" vnf/developer
  The role vnf/developer is in the "group" vnf/user
  The role vnf/user has the privilege "simulation/run"



API
---

To find out if a user has a privilege, do ::
   
  >>> director.accesscontrol.checkPrivilege(target, name)

the privilege is represented by the target and the name.

Example ::

 >>> director.accesscontrol.checkPrivilege('simulation', 'run')


Private records
---------------
Users can label records as private. This will result
in a record in the "labels" db table, while the dom of "labels"
is defined as::

  from OwnedObject import OwnedObject as base
  class Label(base):

    name = 'labels'

    import dsaw.db
    
    labelname = dsaw.db.varchar(name='labelname', length=64)
    entity = dsaw.db.versatileReference(name = 'entity')
    targettable = dsaw.db.varchar(name='targettable', length=64)

For example, if a user declare an experiment as private,
then a new record appears in the "labels" table:

 - labelname='private'
 - entity=<global address of the experiment>

Operations of managing the "private" label are implemented
in content/components/dom-access/label.odb.

 * markAsPrivate(entity): mark a record as private

Convenient methods for db queries are implemented in
vnfb.utils.query.accesscontrol.

TODO: list all methods to present the full API.
