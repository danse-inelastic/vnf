.. _bvk-model:

Create a BvK Model
==================

To create a BvK model, first search for the atomic structure of interest:

.. image:: /shots/bvk/search-atomic-structure.png
   :width: 300px

and click on the structure link in the table.

.. note::
   You can also create a new structure by clicking the "new" button
   on the top right corner of the atomic structure table view page.


Next, in the view of the atomic structure of interest (in this
tutorial, fcc Ni at 296):

.. image:: /shots/bvk/fccNi-view.png
   :width: 650px

Expand the "BvK models" panel near the bottom:

.. image:: /shots/bvk/fccNi-bvk-models-panel.png
   :width: 650px

Click on the "create a new model" link and the bvk model builder
shows up:

.. image:: /shots/bvk/bvkmodel-builder-start.png
   :width: 650px

Please input information 

* reference: source of this model. such as journal paper.
* description: short description of the model
* uses primitive unitcell: whether to use primitve unitcell when you describe your bvk model. If you are not sure, just leave it as is for now
* details: detailed description of this model

Then click the save button, and the page change into:

.. image:: /shots/bvk/bvkmodel-builder-info-saved.png
   :width: 650px

Now in the "Bonds" panel, click "Append a new item", and we got

.. image:: /shots/bvk/bvkmodel-builder-bond-editor.png
   :width: 650px

Here we need to specify a "bond". 

For example, let us say we want to specify a bond between 
the nearest neighbors in fcc Ni.

Since we already chose to use the primitve unit cell,
in this fcc Ni structure Atom 1 is fixed to Ni at (0,0,0).

The atom 2 can be Ni at (0,0,0) with an offset of (0, 1.76, 1.76) in
cartesian coordinates. 
The form requires that the offset to be represented in terms
of basis vectors (which are shown in the Atom 2 offset panel), 
so the offset vector should be (0, 1, 0).

After you enter (0, 1, 0) into the Atom 2 offset field,
you will see the constraint of force constant matrix changes into:

.. image:: /shots/bvk/bvkmodel-builder-constraints.png
   :width: 650px

Suppose that we know the force constant matrix is like::

 xx = yy = 17.72
 xy = yx = 18.735
 zz = -1.015

Compare this with the constraints, then we know that the force 
constant matrix should be (you need to be careful here to 
change the cartesian coordinates a bit since the force constant
matrix you have at hand might be slightly different but actually
related to the bond here with symmetry operation. For example in
this case, change z to x, x to y, and y to z. If you use the constraints
as the reference, it should be easy to figure out.):

.. image:: /shots/bvk/bvkmodel-builder-force-constant-matrix.png
   :width: 650px

Then click the "save" button to save the bond.
If you input incorrectly and violates the symmetry requirement
shown in the "constraints" box, it will alert you.

After saving, you will get:

.. image:: /shots/bvk/bvkmodel-builder-bond-saved.png
   :width: 650px

You can now append a new bond by clicking "Append a new item".

You could also delete a bond by clicking "Delte this item".

After you are done with all bonds for your model, click "I am done" 
button at the bottom.

Congratulations!!! 
