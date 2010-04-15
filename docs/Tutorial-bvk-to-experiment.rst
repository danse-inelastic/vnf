.. _tutorial-bvk-to-experiment:

Tutorial: a virtual neutron experiment using phonon data calculated from BvK model
==================================================================================

In this tutorial, we will show step-by-step how to run a virtual neutron expriment
using a simple sample with coherent inelastic scattering from sample phonons
that are computed from a BvK model.

We start from log in.

Log in
------

Point your browser to https://vnf.caltech.edu/vnf/beta

Then login with your username and password.


Atomic structure
----------------
In this tab, you will see a table of atomic structures.

.. image:: shots/atomicstructure/table-top.png
   :width: 720px


Search for "Al*" for "chemical_formula", and select "fcc Al at 300".



Work flow
---------

 * login
 * minimize help (then click on various "about" menu to get more info)
 * go through all "tabs" to get a feeling of what they are
 * back to atomic structure table. play with "my structures" and "all
   structures"
 * search "\*Al\*" using "description"
 * select fcc Al at 300K

In structure overview, 
 * hover mouse over "structure", "spacegroup" etc
 * expand "Phonons" panel
 * start a new phonons simulation


In phonons simulation wizard:
 * select bvk engine
 * choose the bvk model from literature (expand/shrink different panels)
 * input N1 and df for bvk phonons computation
 * submite job. watch job to be submitted
 * job is finished.


In job view of bvk computation:
 * pack job dir, download. take a look
 * switch to bvk computation. load results. load computed phonons
 * switch to atomic structure (fcc Al). see new results there


Sample
 * create new sample
 * input basic info
 * select atomic structure (table can also be sorted and filtered)
 * select and configure shape
 * add a phonon kernel


experiment
 * start new
 * instrument
  * select ARCS, show large number of components
  * show we can change component
  * back to select Ideal INS.
  * change source to neutrons saved at just before ARCS sample position
  * change sample position and monitor position to 0,0,0
  * change IQEmonitor to use Ei=60
 * sample configuration
  * select a sample
  * further configuration of kernel. make sure ei=60
 * sampele environment
 * review and finish up


