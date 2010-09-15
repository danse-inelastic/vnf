.. _vnfdeveloperguideneutronexperimentsimulation:

Simulations of Neutron Experiments
==================================


Support a new component
-----------------------

DOM
^^^
Add a data object to vnfb.dom.neutron_experiment_simulations.neutron_components.


Job builder
^^^^^^^^^^^
Modify vnfb.components.job_builders.neutronexperiment.InstrumentSimulationAppBuilder


Test job builder
^^^^^^^^^^^^^^^^
Run test by::

 $ cd vnfb/tests/content/components/job_builders/neutronexperiment
 $ python testneutroncomponent.py --component=<new-component-name>



