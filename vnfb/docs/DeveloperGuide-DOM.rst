.. _vnfdeveloperguidedom:

Data object model
=================


data object
-----------
We will use the same data object in :ref:`Support a new computation type <vnfdeveloperguidenewcomputationtype>` as an example. ::


 # this implementation is just for illustration of design.
 class SinIQModel:
  bg = 0.
  amplitude = 1.
  L = 1.
  phase = 0.
  def __call__(self, Q):
    from math import sin
    return self.bg + self.amplitude * sin(self.L * Q + self.phase)**2




Descriptors
-----------
In order to map this data object to a db relation, and create user interface
forms for this data object, we should create a descriptive specification
of the data object. 
In VNF, this is done by creating an
Inventory class and add descriptors for data members::


 from dsaw.model.Inventory import Inventory as InvBase
 class SinIQModelInventory(InvBase):

    bg = InvBase.d.float(name='bg', default=0)
    amplitude = InvBase.d.float(name='amplitude', default=0)
    L = InvBase.d.float(name='L', default=0)
    phase = InvBase.d.float(name='phase', default=0)

This descriptor::

    bg = InvBase.d.float(name='bg', default=0)

specify that "bg" is a float variable, and defaults to 0.

We can add more details of this descriptor, for example,
a tip to developers and users what it is::

    bg.tip = "background noise level"

When this data object is automatically rendered into forms,
this "tip" will show up when users hover his/her mouse
over the UI widget for "bg".


db initializer
--------------

Add a db initializer to content/components/initdb/.

Register the initializer in content/components/initdb/getinitializers.odb

