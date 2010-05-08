.. _tutorial-bvk-to-experiment:

Tutorial: a virtual neutron experiment using phonon data calculated from BvK model
==================================================================================

In this tutorial, we will show step-by-step how to run a virtual neutron expriment
using a simple sample with coherent inelastic scattering from sample phonons
that are computed from a BvK model.

Summary
-------

Starting up and atomic structure:

* :ref:`login <tut-bvk2exp-login>`
* If necessary, :ref:`minimize help window <tut-bvk2exp-minimizehelp>`
* :ref:`select fcc Al at 300K from the atomic structure table <tut-bvk2exp-selectAl300K>`
..   (then click on various "about" menu to get more info)
.. * go through all "tabs" to get a feeling of what they are
.. * back to atomic structure table. play with "my structures" and "all
   structures"

In the :ref:`overview of atomic structure for Al at 300K
<tut-bvk2exp-alat300K>`, 

* :ref:`expand "Phonons" panel <tut-bvk2exp-expandphononpanel>`
* :ref:`start a new phonons simulation <tut-bvk2exp-startnewphononsim>`


In phonons simulation wizard:

* :ref:`select bvk engine <tut-bvk2exp-selectphononengine-bvk>`
* :ref:`choose the bvk model from literature <tut-bvk2exp-selectbvkmodel>`
* :ref:`input N1 and df for bvk phonons computation <tut-bvk2exp-inputbvkparams>`

BvK computation job:

* :ref:`submit job <tut-bvk2exp-submitjob>`
* :ref:`pack job dir <tut-bvk2exp-packjobdir>`
* :ref:`switch to bvk computation view and load results <tut-bvk2exp-bvkcomputation-view>`
* :ref:`switch to atomic structure (fcc Al) <tut-bvk2exp-backtoatomicstructure>`


Sample

* :ref:`create new sample <tut-bvk2exp-newsample-description>`
* :ref:`select atomic structure (table can also be sorted and filtered) <tut-bvk2exp-newsample-atomicstructure>`
* :ref:`select and configure shape <tut-bvk2exp-newsample-shape>`
* :ref:`add a phonon kernel <tut-bvk2exp-newsample-kernel>`


Experiment

* :ref:`start a new experiment <tut-bvk2exp-experiment-new>`
* :ref:`configure instrument <tut-bvk2exp-experiment-selectinstrument>`
* :ref:`configure sample <tut-bvk2exp-experiment-selectsample>`
* :ref:`configure sample environment <tut-bvk2exp-experiment-sampleenvironement>`
* :ref:`review and finish up <tut-bvk2exp-experiment-finish>`



We start with logging in.

.. _tut-bvk2exp-login:

Log in
------

Point your browser to https://vnf.caltech.edu

Then login with your username and password.

.. image:: /shots/login.png
   :width: 400px


The main vnf view will show up.

.. _tut-bvk2exp-minimizehelp:

Minmize help window
^^^^^^^^^^^^^^^^^^^

A help window could show up with the main vnf view. You can minimize
it by clicking the minimize button:

.. image:: /shots/minimize.png
   :width: 100px


Atomic structure
----------------

In the "atomic structure" tab, you will see a table of atomic structures.

.. image:: /shots/atomicstructure/table-top.png
   :width: 720px


.. _tut-bvk2exp-selectAl300K:

Select Al at 300K
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
First we search for "Al*" for "chemical_formula"

.. image:: /shots/atomicstructure/search-Al.png
   :width: 720px


then we choose "fcc Al at 300":

.. image:: /shots/atomicstructure/select-Al300K.png
   :width: 720px


.. _tut-bvk2exp-alat300K:

Atomic structure "Al at 300K"
-----------------------------

We are now in the view of the atomic structure "Al at 300K":

.. image:: /shots/atomicstructure/overview-allcollapsed.png
   :width: 720px

In which there is a panel for computed properties for this material.


.. _tut-bvk2exp-expandphononpanel:

Expand "Phonons" panel
^^^^^^^^^^^^^^^^^^^^^^
Click on the "V" to show the "Phonons" panel:

.. image:: /shots/atomicstructure/Al300K-expand-phonons-panel.png
   :width: 720px


.. _tut-bvk2exp-startnewphononsim:

Start a new phonons simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In the "Phonons" panel,

.. image:: /shots/atomicstructure/Al-phonons-highlight-new-phonon-computation-link.png
   :width: 600px

click on "Start a new phonon computation", and we will be led into a
wizard for simulating phonons.


.. _tut-bvk2exp-phononsimwizard:

Phonons simulation wizard
-------------------------

.. _tut-bvk2exp-selectphononengine-bvk:

Select bvk engine
^^^^^^^^^^^^^^^^^

In the starting page of the phonon simulation wizard:

.. image:: /shots/bvk/phonon-wizard-start.png
   :width: 480px

please select "bvk" as the engine, and click "OK" to continue.

.. _tut-bvk2exp-selectbvkmodel:

Choose a bvk model
^^^^^^^^^^^^^^^^^^

Please choose the bvk model from literature (you could expand the
model panel for details about the model if you like):

.. image:: /shots/bvk/selectmodel.png
   :width: 700px


.. _tut-bvk2exp-selectcomputationtarget:

Choose a computation target
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Please choose to calculate "Phonons on a grid" and click "OK" button

.. image:: /shots/bvk/select-computation-target.png
   :width: 460px


.. _tut-bvk2exp-inputbvkparams:

Input parameters for bvk phonons computation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please input parameters for bvk phonons computation as shown below:

.. image:: /shots/bvk/phonons-computation-params.png
   :width: 460px

After this step, a computation job is created for you.

BvK Computation job
-------------------


.. _tut-bvk2exp-submitjob:

Job submission
^^^^^^^^^^^^^^
In the following form you can configure the computation job:

.. image:: /shots/bvk/submit-job.png

here we don't actually need to change anything, just click "submit",
and you will see the progress of the job submission:

.. image:: /shots/bvk/submitting-job.png


.. _tut-bvk2exp-packjobdir:

Pack job directory
^^^^^^^^^^^^^^^^^^
In the job view

.. image:: /shots/bvk/job-finished.png
   :width: 460px

Click "Pack the job ..." button to watch the job being packed for
download.
After job packing is done, a download link will show up

.. image:: /shots/bvk/download-link.png

click the link to download the file; 
it contains the job directory
where the computation was run.


Now, back to the job view,

.. image:: /shots/bvk/job-results-toswitchtobvkcomputationview.png

click on the button "switch to view of ..." to see the details of the
bvk computation.


.. _tut-bvk2exp-bvkcomputation-view:

BvK Computation View
^^^^^^^^^^^^^^^^^^^^
We are now presented with a view of the bvk computation we just
performed:

.. image:: /shots/bvk/bvk-computation-view.png

as shown above, expand the "Results" panel, and vnf will be retrieving
computation results from server, and soon you will see a plot
of phonon dispersions of fcc Al:

.. image:: /shots/bvk/bvk-computation-result-plot.png

.. _tut-bvk2exp-backtoatomicstructure:

Back to atomic structure of fcc Al
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Now click on the atomic structure link in the "material" panel:

.. image:: /shots/bvk/bvk-computation-view-togobacktoatomicstructure.png

to go back to the view of atomic structure  "Al at 300K", in which you
could expand the "phonons" panel again to see the new computation
results show up.



Create a sample
---------------
On the main menu on the left side:

.. image:: /shots/bvk/main-portlet-select-samples.png

Click on "samples" to view a table of samples in the system:

.. image:: /shots/bvk/samples-new.png

Then click the "new" button on the top toolbar to create a new sample.


.. _tut-bvk2exp-newsample-description:

Sample description
^^^^^^^^^^^^^^^^^^
In the new sample creation form, the first step is to give the sample
a description:

.. image:: /shots/bvk/new-sample-description.png

Please input a description of the new sample, such as "fcc Al plate",
and click "save" button.


.. _tut-bvk2exp-newsample-atomicstructure:

Select atomic structure
^^^^^^^^^^^^^^^^^^^^^^^

The next step is to select the atomic structure for the sample:

.. image:: /shots/bvk/new-sample-select-material.png

Here you could filter the list of atomic structures by looking for
"\*Al\*" for "description", and then select the "fcc Al at 300"
structure, and then click the "select" button.


.. _tut-bvk2exp-newsample-shape:

Select and configure shape
^^^^^^^^^^^^^^^^^^^^^^^^^^

To configure the shape of the sample, click the "box" button
and input the dimensions, and then click the "save" button:

.. image:: /shots/bvk/new-sample-configure-shape.png


.. _tut-bvk2exp-newsample-kernel:

Add a phonon kernel
^^^^^^^^^^^^^^^^^^^
To give the sample scattering properties, please add a kernel.

First, click on the "add a kernel" button

.. image:: /shots/bvk/new-sample-configure-kernel-addakernel.png

Then you can edit the new kernel:

.. image:: /shots/bvk/new-sample-configure-kernel-editkernel.png

Here, we start with clicking the button that looks like a phonon
dispersion near the top, and then choose a computed phonon 
(each choice represented a computed full-phonon-dispersion-set
for the atomic structure we choose earlier), and then click the
"save" button.

When the following panel shows up, we are done with editing this
sample:

.. image:: /shots/bvk/new-sample-configure-kernel-done.png


.. _tut-bvk2exp-experiment:

Run a virtual neutron experiment using the new sample
-----------------------------------------------------

Select on the "experiments" of the main menu on the left side:

.. image:: /shots/bvk/main-portlet-select-experiments.png


.. _tut-bvk2exp-experiment-new:

Start a new experiment
^^^^^^^^^^^^^^^^^^^^^^

Let us create a new experiment by clicking the "new" button 
on the toolbar near the top:

.. image:: /shots/bvk/experiments-new.png


.. _tut-bvk2exp-experiment-selectinstrument:

Choose and Configure instrument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Select the "Ideal Inelastic Neutron Scattering Instrument ..." and
click the "continue" button:

.. image:: /shots/bvk/experiment-select-idealins.png

In the configuration panel for the source component of this
instrument,
click on the "change component type" selector and choose
"NeutronPlayer" from the list:

.. image:: /shots/bvk/experiment-instrument-change-source-type.png

Now click the "edit" link in the new panel for the neutron player:

.. image:: /shots/bvk/experiment-instrument-source-edit.png

Near the bottom of the form for configuring the neutron player, click 
on the selector for "Neutrons"  to select the item
"neutrons at sample position of ARCS instrument. Ei~60meV".

.. image:: /shots/bvk/experiment-instrument-neutronplayer-choose-neutrons.png

A panel with information of first few neutrons in the neutron storage
will show up. Click the "save" button to continue.

.. image:: /shots/bvk/experiment-instrument-neutronplayer-selected-neutrons-and-save.png

Now select the "sample" component from the component chain:

.. image:: /shots/bvk/experiment-instrument-to-select-samplecomponent.png

Again, click the "edit" link, and in the form for the sample
component, make sure to change position of the sample to (0,0,0),
and then click the "save" button.

.. image:: /shots/bvk/experiment-instrument-sample-position.png

Next, let us turn to the last component, "monitor":

.. image:: /shots/bvk/experiment-instrument-to-select-monitorcomponent.png

Click the "edit" link and make sure to change the position of the
monitor to (0,0,0) and Ei to 60.0 meV.

.. image:: /shots/bvk/experiment-instrument-monitor-config.png

and click the "save" button to save your changes

.. image:: /shots/bvk/experiment-instrument-monitor-saveconfig.png

Now we are done with configuration of the instrument, just click the
"continue" button

.. image:: /shots/bvk/experiment-instrument-done.png


.. _tut-bvk2exp-experiment-selectsample:

Choose and Configure Sample
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Please select the sample you created earlier and click the "continue"
button.
Again, you can use the filter control to find your sample.

.. image:: /shots/bvk/experiment-select-sample.png

We need to slightly change the kernel configuration. Click the "edit"
button
as shown below:

.. image:: /shots/bvk/experiment-sample-toeditkernel.png

and change Ei to 60 meV and click the "save" button.

.. image:: /shots/bvk/experiment-sample-editkernel.png

Now we are done with configuration of the sample, just click the
"continue" button 

.. image:: /shots/bvk/experiment-sample-done.png

.. _tut-bvk2exp-experiment-sampleenvironement:

Configure sample environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There is not much to do with sample environment at this point;
just click the "save" button and then the "continue" button:

.. image:: /shots/bvk/experiment-sampleenv-done.png


.. _tut-bvk2exp-experiment-finish:

Review and finish up
^^^^^^^^^^^^^^^^^^^^

This is the last step for setting up an experiment.
Please give the experiment a description and click the
"save" button and then the "continue" button.

.. image:: /shots/bvk/experiment-finish-config.png

You will be presented with a summary of the experiment.
Click on the "^" symbol on the left top corner of the panel
to shrink the panel down

.. image:: /shots/bvk/experiment-finish-summary.png

Click the "create job" button to create the computation job for 
this experiment.

.. image:: /shots/bvk/experiment-finish-tocreatejob.png

The job configuration form shows up; please give the computation
job a description and then click the "submit" button

.. image:: /shots/bvk/experiment-job-config.png

This job will take a moment to submit. After submission, 
a panel for the job will show up. You can click the "refresh"
button to update that view. 
When the job is done, click on 
the button "switch to the view of ..." to view the neutron experiment.

.. image:: /shots/bvk/experiment-jobview-toswitchtoexp.png

In the neutron experiment view, expand the "results" panel
and then the "histogram" panel inside, you will get a view of the 
I(Q,E) spectrum recorded by the virtual monitor:

.. image:: /shots/bvk/experiment-view-results-expanded.png

