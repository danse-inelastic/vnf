.. _vnfdeveloperguideneutronexperimentsimulation:

Simulations of Neutron Experiments
==================================


Support a new component
-----------------------

DOM
^^^
Add a data object to vnf.dom.neutron_experiment_simulations.neutron_components.


Job builder
^^^^^^^^^^^
Modify vnf.components.job_builders.neutronexperiment.InstrumentSimulationAppBuilder


Test job builder
^^^^^^^^^^^^^^^^
Run test by::

 $ cd vnf/tests/content/components/job_builders/neutronexperiment
 $ python testneutroncomponent.py --component=<new-component-name>



Instrument
----------


Create an instrument
^^^^^^^^^^^^^^^^^^^^
Developers and sys admins can create instruments from script.




How to upgrade an instrument?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, you will find a better implementation of an instrument
(for example, inserting a new component into the component chain
that was ignored previously), and want to upgrade an instrument.
The way to do it is to create a new instrument and call it 
with the same name as before, and take the old instrument offline
(unless you really want to have more than one versions of
the same instrument shown to users of VNF, which might be confusing).

