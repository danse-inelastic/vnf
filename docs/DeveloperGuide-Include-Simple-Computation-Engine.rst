.. _vnfdeveloperguidenewcomputationtype:

Support a new type of computation
=================================

Say we want to support a simple calculator that calculates I(Q) from a simple function::

 I(Q): bg + amplitude * sin(L*Q + phase)**2

where the following are parameters

- bg: background
- amplitude: 
- L: 
- phase:

The goal is to calculate a I(Q) curve from this simple model.

Initial Analysis
----------------

This problem can be easily structured as two pieces: a model and a computation based on this model. The model is simply a functor that describes the I(Q) functional form, and the computation part actually is a general evaluation engine to evaluate value of I(Q) at given points of interests. ::

 # this implementation is just for illustration of design.
 class SinIQModel:
  bg = 0.
  amplitude = 1.
  L = 1.
  phase = 0.
  def __call__(self, Q):
    from math import sin
    return self.bg + self.amplitude * sin(self.L * Q + self.phase)**2
 
 

 class IQModelEvaluation:
  model = SinIQModel()
  Qmin = 0
  Qmax = 10
  dQ = 0.1

  def __call__(self):
    Qmax = self.Qmax; Qmin = self.Qmin; dQ = self.dQ
    n = int((Qmax-Qmin)/dQ)
    return [self.model(Qmin+dQ*i) for i in range(n)]


Map to db
---------
We use an object relational mapper (ORM) to map data objects 
to db tables for relational data base. 
More details about our orm can be found in 
http://docs.danse.us/pyre/sphinx/pyreLibraries.html#extending-the-capabilities-of-pyre-db-dsaw-db


DB tables are used to store user iinputs about computations. Here,
we need two db tables, each for one data object type. 
The mapping could be as easy as ::

 from dsaw.model.visitors.Object2DBTable import Object2DBTable
 o2t = Object2DBTable()
 SinIQModelTable = o2t(SinIQModel)
 IQModelEvaluationTable = o2t(IQModelEvaluation)

More details
""""""""""""
You could decorate the original class with a bit more information (meta data)
so that the mapping can be more precise (otherwise, orm will have to guess 
from your class definition).

The way of decoration is to add an "Inventory" class to the class definitions
of the data objects. ::

 from dsaw.model.Inventory import Inventory as InvBase
 class SinIQModelInventory(InvBase):

    bg = InvBase.d.float(name='bg', default=0)
    amplitude = InvBase.d.float(name='amplitude', default=0)
    L = InvBase.d.float(name='L', default=0)
    phase = InvBase.d.float(name='phase', default=0)

 class SimpleIQComputation(base):

    model = InvBase.d.reference(name='model', type=SinIQModel)
    Qmin = InvBase.d.float(name='Qmin', default=0)
    Qmax = InvBase.d.float(name='Qmax', default=10)
    dQ = InvBase.d.float(name='dQ', default=0.1)

and then the mapping can be more precise::

 from dsaw.model.visitors.Object2DBTable import Object2DBTable
 o2t = Object2DBTable()
 SinIQModelTable = o2t(SinIQModel)
 IQModelEvaluationTable = o2t(IQModelEvaluation)

User interface
--------------
Next we need to build forms for user to configure their computations. 

Luban orm will help you do that. You will need to drop components
into content/components/actors/orm 
(http://danse.us/trac/VNET/browser/vnf/trunk/content/components/actors/orm)::
 
 # siniqmodels.odb
 from vnf.dom...SinIQModel import SinIQModel
 import luban.orm
 Actor = luban.orm.object2actor(SinIQModel)
 def actor():
    return Actor('orm/siniqmodels')

and ::

 # iqmodelevaluations.odb
 from vnf.dom...IQModelEvaluation import IQModelEvaluation
 import luban.orm
 Actor = luban.orm.object2actor(IQModelEvaluation)
 def actor():
    return Actor('orm/iqmodelevaluations.odb')


Try it out
""""""""""
Now you can try it out! You can try it out by using command line::

 $ main.cgi --actor=orm/siniqmodels

or using browser:

http://your.dev.site/cgi-bin/vnf/main.cgi?actor=orm/siniqmodels&routine=debug_edit


Computation
-----------

For this simple computation, you may simply run the __call__ method
of the IQModelEvaluation class and present the result to users,
but most computation we deal with are more complex and need more
computing resources. The latter case must be dealt with using a job 
builder.

Job builder
"""""""""""
A job builder takes a computation db record and converts it into a script that can be run by itself. 
An example is
http://danse.us/trac/VNET/browser/vnf/trunk/content/components/job_builders/material_simulations/phonon_calculators/bvk_getdos.odb



Improve your work flow
----------------------
Wizard to set up a computation
""""""""""""""""""""""""""""""

