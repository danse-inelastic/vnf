.. _vnfuserguideoverview:

Overview
========

Virtual neutron facility is a web service where you can plan 
and run virtual neutron experiments, 
and collect virtual experiment data for your virtual sample.
In a virtual neutron experiment, virtual neutrons are generated from a
virtual neutron source, guided by virtual neutron guides, scattered by
a virtual sample and sample environment, and intercepted by virtual detectors.

You can perform your experiments on a variety of neutron instruments, both
actual physical instruments and conceptual instruments.

You can also create your sample and predict its neutron scattering
properties  by calculating its structure or dynamics. For example, the
material behaviors calculated by ab initio or molecular dynamics
methods become scattering kernels that can be used in the sample
simulation part of your virtual experiment.

.. image:: shots/main-interface-example-exptable.png
   :width: 780px

The user interface of VNF has an overall uniform structure:
the main interface is organized as tabs, of which several 
menu items are on the left side of the screen,
linking to a variety of functions. 
In each tab, the main view is a table of entities such as
atomic structures, experiments, or computational jobs.
Also presented in the main view of a tab are controls to
create a new entity, to navigate, sort and search the table, 
and to tag entities with labels for easier organization
(More details of these controls are explained
:ref:`using the "atomic structures" tab as the example <atomic-structures>`).

Another principle of the VNF user interface is to show the interconnections
of entities. For example, in the view of an atomic structure, you 
should be able to see (links to) entities related this atomic structure,
for example, its phonon density of states computed from a bvk
computation; in a view of a computation job, there will be a link 
that can bring you to the view of the computation that job is about.

At this moment, you may want to explore VNF a little bit.
For example, you
can review past experiments by clicking 
:ref:`"Experiments" <exps-tab>`, 
or browse your
personal library of samples by clicking 
:ref:`"Samples" <samples-tab>`. 
A library of
materials you and other researchers are interested are in the tab
:ref:`"Atomic structures" <atomic-structures>`.
You can try to 
start a virtual experiment [#start-exp]_ ,
or a material simulation [#start-mat-sims]_ , 
and they can
become computational jobs to be submitted to computing resources. 
You can monitor their progress by clicking "Jobs".

For a quick start, you may want to 
watch some videos, and
follow some tutorials:

* :ref:`Video clips of typical workflows <screencasts>`
* :ref:`Tutorials <userguide-tutorials>`


Detailed explanations of all tabs are also available

* :ref:`Atomic structures <atomic-structures>`
* :ref:`Material simulations <matsim-tab>`
* :ref:`Analysis <analysis-tab>`
* :ref:`Samples <samples-tab>`
* :ref:`Experiments <exps-tab>`
* :ref:`Jobs <jobs-tab>`

.. rubric:: Footnotes

.. [#start-exp] See  
   :ref:`virtual experiment tutorials <exp-tutorials>`, 
   and also video demos, e.g.
   `Video: inelastic scattering of lead plate <http://www.youtube.com/watch?v=puHiA4qcL7U&fmt=22>`_
.. [#start-mat-sims] Video demos, e.g. 
   `Quantum Espresso workflow <http://docs.danse.us/VNET/movies/qe.html>`_, 
   `Lead phonon dispersions from bvk  <http://www.youtube.com/watch?v=3BYNlvENz_k&fmt=22>`_,
   `Forcefield simulation and S(Q,E) generation--setup (with audio) <http://docs.danse.us/VNET/movies/st_screencast.mov>`_
