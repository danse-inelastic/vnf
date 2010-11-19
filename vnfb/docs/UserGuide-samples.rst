.. _samples-tab:

Samples
=======

In this tab, a table of virtual samples are presented.

Samples are the core of neutron experiments. In this tab,
you can create a new sample, and also search and learn details
of previously created samples.

.. image:: shots/samples/table-top.png
   :width: 720px


To see how to sort, filter, and how to use labels, please read
:ref:`the table view section <atomic-structures-tableview>` for 
:ref:`atomic structures <atomic-structures>` first. The basic 
functionalities of the table view here is the same as the one
for atomic structures.


What is a sample
----------------
In VNF, a sample is a neutron scatterer with a shape. 
The neutron scatterer consists of homogeneously distributed
material (or can be regarded as homogenesously distributed in 
some averaging scheme)
within the shape.

A neutron scatterer can have multiple scattering kernels, 
each of which scatter neutrons in a way that is independent
of the position of scattering inside the shape of the scatterer.


How to create a sample
----------------------
Here we will try to create a polycrystalline Fe plate sample with
phonon inelastic scattering kernel.

To create a sample, first click the "new" button at the
top-right corner of the "sample" page:

.. image:: shots/samples/new-button.png
   :width: 580px


Then input a description of your sample in the "description"
input text box, and click the "save" button.

.. image:: shots/samples/editdescription.png
   :width: 280px


Now we need to select an atomic structure for the sample.
From within the filter/search toolbox, please select "description" 
and input "\*Fe\*", 

.. image:: shots/samples/search-for-fe.png
   :width: 500px

and hit **Enter** key 
to search for Fe related structures:

.. image:: shots/samples/select-material.png
   :width: 500px

Select the "bcc Fe at 295K" material and click the select button,
you will see an overview of the material:

.. image:: shots/samples/material-view.png
   :width: 500px

Now you can move on to the shape panel,

.. image:: shots/samples/shape-panel.png
   :width: 300px

and click on one of the shape icons. A form for editing the
shape will come up. The default configuratioin there is 
for a plate. Please click the "save" button after configuration:

.. image:: shots/samples/edit-block.png
   :width: 200px

and an overview of the configured shape shows up:

.. image:: shots/samples/block-overview.png
   :width: 200px

Now our focus is to provide the sample neutron scattering 
properties. This will be done in the "kernels" panel:

.. image:: shots/samples/kernels-panel.png
   :width: 600px

Click "add a kernel" button to add a new kernel.
A few icons of kernel types show up, and please
click on the "isotropic elastic kernel" type:

.. image:: shots/samples/select-a-kernel-type.png
   :width: 300px

Click the "Save" button to save your configuration:

.. image:: shots/samples/configure-isotropic-kernel.png
   :width: 400px


And you are now done with creating a sample with an isotropic
neutron scattering kernel. You can add more kernels to the sample,
if you want:

.. image:: shots/samples/add-more-kernel.png
   :width: 450px
