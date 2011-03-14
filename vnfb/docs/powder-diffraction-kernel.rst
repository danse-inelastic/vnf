.. _powder-diffraction-kernel:

Using Powder Diffraction Kernel in VNF
======================================================

Introduction
------------

In this tutorial we will learn how to use Powder Diffraction Kernel for simple
instrument composed of three componentsin in VNF:

::

[SimpleSource] -> [SampleComponent] -> [EMonitor]

``SimpleSource`` generates beam of neutrons uniformly distributed within the energy range
``[E0-dE, E0+dE]`` which are scattered by ``SampleComponent`` with the powder
diffraction kernel inside. Neutrons scattered by the ``SampleComponent`` are detected by the
``EMonitor`` - the energy sensitive monitor. As a result we should see distinctive
peaks on the Intensity vs. Energy I(E) plot.

Create New Sample
-----------------

To explore the diffraction properties of material we create the new
sample which includes the powder diffraction kernel. In the tab *Sample*
click on the *Create New Sample* button.

.. figure:: images/powder-diff-kernel/1.sample-list.png
   :width: 720px

   *Fig. 1 Create new sample*

To configure sample one needs to fill out several sections:

* Basic information
* Atomic structure
* Geometry shape
* Kernels

Let's start with the ``Basic information`` section. In this section all you need
to set is the ``description``. This description can be important to help you find
this experiment later on. Once the description is set don't forget to click on
``Save`` button.

.. figure:: images/powder-diff-kernel/2.sample-description.png
   :width: 300px

   *Fig. 2 Edit sample description*


.. figure:: images/powder-diff-kernel/3.sample-structure.png
   :width: 720px

   *Fig. 3 Select atomic structure*

.. figure:: images/powder-diff-kernel/4.sample-shape.png
   :width: 300px

   *Fig. 4 Select and edit sample shape*



Add Powder Diffraction Kernel
--------------------------------

.. figure:: images/powder-diff-kernel/5.sample-kernel-add.png
   :width: 720px

   *Fig. 5 Select Powder Diffraction Kernel*

.. figure:: images/powder-diff-kernel/6.sample-kernel-form.png
   :width: 520px

   *Fig. 6 Edit parameters for the kernel*

.. figure:: images/powder-diff-kernel/7.sample-kernel-created.png
   :width: 720px

   *Fig. 7 Powder Diffraction Kernel information*

.. figure:: images/powder-diff-kernel/8.sample-kernel-info-full.png
   :width: 720px

   *Fig. 8 Final sample configuration*


Create New Instrument
---------------------


.. figure:: images/powder-diff-kernel/9.experiment-new.png
   :width: 720px

   *Fig. 9 Create new instrument*

.. figure:: images/powder-diff-kernel/10.instrument-select.png
   :width: 720px

   *Fig. 10 Select instrument type*

.. figure:: images/powder-diff-kernel/11.instrument-chain.png
   :width: 720px

   *Fig. 11 Instrument component chain*


Instrument Components Configuration
-----------------------------------

.. figure:: images/powder-diff-kernel/12.source-parameters.png
   :width: 450px

   *Fig. 12 Edit SimpleSource configuration*

.. figure:: images/powder-diff-kernel/13.source-info.png
   :width: 720px

   *Fig. 13 SimpleSource configuration*

.. figure:: images/powder-diff-kernel/14.sample-edit.png
   :width: 720px

   *Fig. 14 Edit basic sample configuration*


.. figure:: images/powder-diff-kernel/15.sample-info-chain.png
   :width: 720px

   *Fig. 15 Basic sample configuration*

.. figure:: images/powder-diff-kernel/16.monitor-edit.png
   :width: 300px

   *Fig. 16 Edit EMonitor configuration*

.. figure:: images/powder-diff-kernel/17.monitor-info-chain.png
   :width: 720px

   *Fig. 17 EMonitor configuration*

.. figure:: images/powder-diff-kernel/18.continue-button.png
   :width: 150px

   *Fig. 18 Continue Button*


Sample Configuration
--------------------


.. figure:: images/powder-diff-kernel/19.sample-select.png
   :width: 720px

   *Fig. 19 Select sample for sample component*

.. figure:: images/powder-diff-kernel/20.sample-review.png
   :width: 720px

   *Fig. 20 Review sample configuration*



.. figure:: images/powder-diff-kernel/21.sample-environment.png
   :width: 720px

   *Fig. 21 Sample environment configuration*


Experiment Configuration
------------------------

.. figure:: images/powder-diff-kernel/22.experiment-edit.png
   :width: 450px

   *Fig. 22 Edit basic experiment configuration*

.. figure:: images/powder-diff-kernel/23.experiment-info.png
   :width: 720px

   *Fig. 23 Basic experiment configuration*

.. figure:: images/powder-diff-kernel/24.experiment-review.png
   :width: 400px

   *Fig. 24 Review of full experiment configuration*

.. figure:: images/powder-diff-kernel/25.create-job-button.png
   :width: 150px

   *Fig. 25 Create job*


Job Submission, Monitoring and Results Retrieval
------------------------------------


.. figure:: images/powder-diff-kernel/26.job-form.png
   :width: 350px

   *Fig. 26 Edit experiment job*


.. figure:: images/powder-diff-kernel/27.job-submission.png
   :width: 720px

   *Fig. 27 Job submission*

.. figure:: images/powder-diff-kernel/28.job-running.png
   :width: 480px

   *Fig. 28 Running job*

.. figure:: images/powder-diff-kernel/29.job-finished.png
   :width: 720px

   *Fig. 29 Finished job*

.. figure:: images/powder-diff-kernel/30.job-packing.png
   :width: 720px

   *Fig. 30 Results retrieval*

.. figure:: images/powder-diff-kernel/31.job-tarball.png
   :width: 500px

   *Fig. 31 Results ready for download*


Experiment Results
---------------------

.. figure:: images/powder-diff-kernel/32.experiment-results.png
   :width: 720px

   *Fig. 32 Experiment results*

.. figure:: images/powder-diff-kernel/33.results-histogram.png
   :width: 720px

   *Fig. 33 Histogram I(E)*










