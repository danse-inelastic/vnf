Calculating an S(Q,E) and DOS from md with VNF
======================================================

Introduction
------------

In this short tutorial I will walkthrough the main steps to calculate an SQE scattering kernel in VNF using the Gulp as an md engine.

Create New Simulation
---------------------

Go to the “Simulations” section, click on the “New” green cross like button.

.. figure:: images/mdSqe/1.sim-table.png
   :width: 720px

A table of simulation packages will be displayed with a short description. Click on the “Gulp” link:

.. figure:: images/mdSqe/selectGulp.png
   :width: 450px

You can then select an atomic structure from the list or create a new one from the “Atomic Structure” section.

.. figure:: images/mdSqe/selectMaterial.png
   :width: 450px

Click select and deploy AtomSim by clicking “Launch”.  A Java GUI should appear.  Review the atomic coordinates:

.. figure:: images/mdSqe/coordinates.png
   :width: 720px
   
Review the cell parameters:

.. figure:: images/mdSqe/cellParameters.png
   :width: 720px

Many types of potentials are available in AtomSim.  They can either be accessed by selection from a list or by specifying directly:

.. figure:: images/mdSqe/potentials.png
   :width: 720px
   
   


.. figure:: images/qe-phonon-dos/18.pw-run-task.png
   :width: 400px

   *Fig. 18 PW configuration input is created. Ready to run the task!*

Now we are ready to run the task. All you need to do is just to click on the 
“Run Task” button to submit the simulation to the specified cluster. In our 
example it is foxtrot.danse.us. During this process the job will be created, 
so the configuration and other supporting files will be transferred to the 
computing cluster. The job will be submitted to the jobs queue (e.g. Torque), 
if your cluster supports it, or run directly on the cluster without submitting 
to any queue. 

You can run multiple jobs for one task. It is important to have this feature 
because sometimes jobs fail for a variety of reasons. When the job fails, you 
can check if the configuration file is correct or it is set too many processors 
and too few K-points which will affect the parallelization of the problem. To 
see what's wrong, just retrieve results and see the output and log files. To 
see all jobs, click on the link All Jobs

.. figure:: images/qe-phonon-dos/19.pw-job-submitted.png
   :width: 200px

   *Fig. 19 Job is submitted, results are not requested yet*

Retrieving Results
------------------

When the simulation job is completed it is nice to get the results of the 
simulation :). To retrieve the results, just click on the button “Check”. 
The status of the results packing will be displayed

.. figure:: images/qe-phonon-dos/20.pw-job-completed.png
   :width: 420px

   *Fig. 20 Retrieving simulation results*

Here is the content of the results tarball:

.. figure:: images/qe-phonon-dos/21.pw-tarball.png
   :width: 450px

   *Fig. 21 PW results tar ball*

To avoid the results delivery failure you can try to retrieve results again from 
the computational cluster after 3 min. This feature is implemented to give some 
time for the results to be delivered or in case if the delivery failed.

Running the PH Task
-------------------

Once the PW task is successfully completed you can create PH task and set
configuration input for it.

.. figure:: images/qe-phonon-dos/22.ph-input-add.png
   :width: 600px

   *Fig. 22 Add PH configuration input*

The form will be displayed where you can set the size of Q grid. All parameters 
in this form are required.

.. figure:: images/qe-phonon-dos/23.ph-input-form.png
   :width: 450px

   *Fig. 23 PH configuration input form*

When you click on “Generate Input Configuration” the configuration form is displayed.
As for PW input you can edited the configuration text.

.. figure:: images/qe-phonon-dos/24.ph-input-generated.png
   :width: 450px

   *Fig. 24 PH configuration input form*

When the input is created we are ready to run task.

.. figure:: images/qe-phonon-dos/25.ph-job-completed.png
   :width: 720px

   *Fig. 25 Running PH task and retrieving results*

When the job is completed you can request the results (see section “Retrieving
Results”). The results will be packed in tarball and you can see its content:

.. figure:: images/qe-phonon-dos/26.ph-tarball.png
   :width: 500px

   *Fig. 26 PH results tar ball*


.. figure:: images/qe-phonon-dos/27.ph-output.png
   :width: 720px

   *Fig. 27 PH output file*

Running the Q2R Task

Once the PH task is successfully completed, you can create a Q2R task and set 
the configuration input for it. Q2R and MATDYN tasks are postprocessing tasks

.. figure:: images/qe-phonon-dos/28.q2r-input-add.png
   :width: 720px

   *Fig. 28 Add Q2R configuration input*

The form will be displayed where you can set acoustic sum rules. This parameter 
will be different for metals and dielectrics.

.. figure:: images/qe-phonon-dos/29.q2r-input-form.png
   :width: 500px

   *Fig. 29 Q2R configuration input form*

When you click on “Generate Input Configuration” the configuration form is
displayed and you can edited the configuration text.

.. figure:: images/qe-phonon-dos/30.q2r-input-generated.png
   :width: 500px

   *Fig. 30 Q2R configuration input form*

When the input is created we are ready to run task

.. figure:: images/qe-phonon-dos/31.q2r-job-completed.png
   :width: 720px

   *Fig. 31 Running Q2R task and retrieving results*

When the job is completed you can request the results. The results will be packed 
in tarball and you can see its content:

.. figure:: images/qe-phonon-dos/32.q2r-tarball.png
   :width: 500px

   *Fig. 32 Q2R results tarball.*

Force constants file (``default.fc``) will be used by the MATDYN task to create
the phonon DOS, so make sure that it is present in the results.

Running the MATDYN Task
-----------------------

Once the Q2R task is successfully completed, and has created a force constants
file default.fc you can create a MATDYN task and set the configuration input for it.

.. figure:: images/qe-phonon-dos/33.matdyn-input-add.png
   :width: 720px

   *Fig. 33 Add MATDYN configuration input*

Here you can have two options:

* Phonon Density of States (DOS)
* Phonons on Grid

For purpose of this tutorial we will pick the “Phonon Density of States”.

.. figure:: images/qe-phonon-dos/34.matdyn-dos.png
   :width: 500px

   *Fig. 34 Phonon Density of States*

The form will be displayed where you can set size of the uniform Q-point grid.

.. figure:: images/qe-phonon-dos/35.matdyn-input-form.png
   :width: 500px

   *Fig. 35 MATDYN configuration input form for setting Q-point grid*

When you click on “Generate Input Configuration” the configuration form is
displayed and you can edited the configuration text.

.. figure:: images/qe-phonon-dos/36.matdyn-input-generated.png
   :width: 500px

   *Fig. 36 MATDYN configuration input form*

When the input is created we are ready to run task.

.. figure:: images/qe-phonon-dos/37.matdyn-job-completed.png
   :width: 720px

   *Fig. 37 Running MATDYN task and retrieving results*

When the job is completed you can request the results. The results will be
packed in tarball and you can see its content:

.. figure:: images/qe-phonon-dos/38.matdyn-tarball.png
   :width: 720px

   Fig. 38 MATDYN results tar ball with phonon DOS file (``matdyn.dos``).

At this point we received phonon DOS (``matdyn.dos``) that can later be used to draw a plot.

Results Analysis
----------------

For analysis of the results, we implemented a basic interface that allows you to
display relevant information for the simulation. The alternative way will be to
get the results tarballs retrieved for each of the tasks and use your favorite
tools to analyze data. To do our results analysis of simulation, click on “Analyze”
button.

.. figure:: images/qe-phonon-dos/39.sim-view-completed.png
   :width: 720px

   *Fig. 39 Simulation view after all of the tasks are completed. Time to analyze results!*

The Results panel will displayed that consists of two parts:

* Electron System
* Phonon System

Electron-phonon calculation is not supported on VNF at this time. On the results
panel we can see the “Phonon DOS” plot that we have generated data for recently.
To see the phonon DOS on the atomic structures page, you need to create the phonon
DOS explicitly on the results page by clicking on “Create Phonon DOS” button.
Clicking this button will convert matdyn.dos to IDS (Inelastic Data Storage) format.

.. figure:: images/qe-phonon-dos/40.results-view.png
   :width: 720px

   *Fig. 40 Results view page*

Wuala! The phonon DOS is created! Go to the simulation view page and click on the
link for the Atomic Structure field. In the subsection “Phonons” you will see the
plot for density of states (DOS).

.. figure:: images/qe-phonon-dos/41.phonon-dos.png
   :width: 720px

   *Fig. 41 Phonon DOS on the Atomic Structures page*

